"""
Response Transformer
Transforms AI response format to match frontend expected format
"""


def transform_analysis_response(ai_response):
    """
    Transform AI response to match the original Streamlit format expected by frontend.

    Args:
        ai_response: Raw response from AI service

    Returns:
        dict: Transformed response matching frontend TypeScript interfaces
    """
    if not ai_response.get('success'):
        return ai_response

    data = ai_response.get('data', {})
    transformed_data = {}

    # Transform lab_analysis biomarkers
    if 'lab_analysis' in data:
        lab_analysis = data['lab_analysis']
        transformed_biomarkers = []

        for biomarker in lab_analysis.get('detailed_biomarkers', []):
            # Parse result to extract value and unit
            result_str = biomarker.get('result', '')
            value = result_str
            unit = ''

            # Try to split result into value and unit
            parts = result_str.split()
            if len(parts) >= 2:
                value = parts[0]
                unit = ' '.join(parts[1:])

            transformed_biomarker = {
                'biomarker_name': biomarker.get('name', ''),
                'value': value,
                'unit': unit,
                'reference_range': biomarker.get('range', ''),
                'optimal_range': biomarker.get('range', ''),  # Using same as reference for now
                'status': biomarker.get('status', 'optimal'),
                'interpretation': biomarker.get('why_it_matters', ''),
                'recommendations': []  # AI doesn't provide individual recommendations per biomarker in this format
            }
            transformed_biomarkers.append(transformed_biomarker)

        transformed_data['lab_analysis'] = {
            'biomarkers_tested_count': lab_analysis.get('biomarkers_tested_count', 0),
            'detailed_biomarkers': transformed_biomarkers,
            'biomarker_categories_summary': lab_analysis.get('biomarker_categories_summary', {})
        }

    # Transform four_pillars from array to object format
    if 'four_pillars' in data:
        pillars_data = data['four_pillars']
        pillars_array = pillars_data.get('pillars', [])

        transformed_pillars = {}

        for pillar in pillars_array:
            pillar_name = pillar.get('name', '').lower().replace(' well', '')

            # Extract action items from additional_guidance
            action_items = []
            if 'additional_guidance' in pillar:
                guidance = pillar['additional_guidance']
                if 'structure' in guidance:
                    structure = guidance['structure']
                    # Get recommended items based on pillar type
                    if 'recommended_foods' in structure:
                        action_items = [f"{item['name']}: {item['description']}"
                                       for item in structure['recommended_foods'][:3]]
                    elif 'recommended_workouts' in structure:
                        action_items = [f"{item['name']}: {item['description']}"
                                       for item in structure['recommended_workouts'][:3]]
                    elif 'recommended_recovery_tips' in structure:
                        action_items = [f"{item['name']}: {item['description']}"
                                       for item in structure['recommended_recovery_tips'][:3]]

            transformed_pillars[pillar_name] = {
                'score': pillar.get('score', 0),
                'status': get_pillar_status(pillar.get('score', 0)),
                'summary': pillar.get('science_based_explanation', ''),
                'recommendations': pillar.get('score_rationale', []),
                'action_items': action_items
            }

        transformed_data['four_pillars'] = transformed_pillars

    # Transform supplements
    if 'supplements' in data:
        supplements_data = data['supplements']
        recommendations = []

        if 'structure' in supplements_data and 'recommendations' in supplements_data['structure']:
            for supp in supplements_data['structure']['recommendations']:
                transformed_supp = {
                    'supplement_name': supp.get('name', ''),
                    'dosage': supp.get('dosage_and_timing', ''),
                    'timing': supp.get('dosage_and_timing', ''),
                    'reason': supp.get('rationale', ''),
                    'priority': get_supplement_priority(supp.get('name', '')),
                    'cautions': supp.get('situational_cyclical_considerations', '')
                }
                recommendations.append(transformed_supp)

        transformed_data['supplements'] = {
            'recommended_supplements': recommendations,
            'supplement_summary': supplements_data.get('description', '')
        }

    return {
        'success': True,
        'data': transformed_data,
        'status': ai_response.get('status', [])
    }


def get_pillar_status(score):
    """Get status label based on score"""
    if score >= 8:
        return 'Excellent'
    elif score >= 6:
        return 'Good'
    elif score >= 4:
        return 'Needs Improvement'
    else:
        return 'Needs Attention'


def get_supplement_priority(supplement_name):
    """Determine priority based on supplement name (simplified logic)"""
    high_priority = ['vitamin d', 'd3', 'magnesium']
    medium_priority = ['omega', 'fish oil', 'probiotics']

    name_lower = supplement_name.lower()

    for hp in high_priority:
        if hp in name_lower:
            return 'high'

    for mp in medium_priority:
        if mp in name_lower:
            return 'medium'

    return 'low'
