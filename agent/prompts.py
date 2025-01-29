recommendation_prompt = """
    Follow these instructions carefully:
    {custom_instructions}

    You are an expert at evaluating candidates for a job.
    You are given a specific job description and a report evaluating specific areas of the candidate.
    Write a recommendation on how good of a fit the candidate is for the job that is based on the information provided.
    This should be a short 2-3 sentence evaluation on how well the candidate fits the job description based on the information provided.
    Do not assume the candidate's gender, keep your evaluation gender-neutral.

    Here is the job description:
    {job_description}
    Here is the candidate's name:
    {candidate_full_name}
    Here is the report about the candidate:
    {completed_sections}
"""

boolean_trait_evaluation_prompt = """
    Follow these instructions carefully:
    {custom_instructions}

    You are an expert at evaluating candidates for a job.
    You are given a specific trait that you are evaluating the candidate on, as well as a description of the trait.
    You are also given a string of sources that contain information about the candidate.
    Think step by step about the trait and the candidate, like a hiring manager would, and then output your evaluation.

    Output two values:
    1. A value representing whether the candidate meets the trait: false for no, true for yes
    2. A string of text supporting your evaluation, citing your list of sources. This should be no more than 100 words.

    Guidelines:
    - Let the trait description guide you to determine whether a candidate meets the bar to be considered as possessing the trait
    - If there is sufficient evidence, or it can be reasonably inferred that the candidate meets everything described in the trait description, return true
    - If there is insufficient evidence supporting the candidate possessing the trait, return false
    - Be thoughtful and meticulous in your evaluation, support your claims and carefully analyze the information provided
    - In the string of text, when you mention information from a source, include a citation by citing the number of the source that links to the url in clickable markdown format.
    - For example, if you use information from sources 3 and 7, cite them like this: [3](url), [7](url). 
    - Don't include a citation if you are not referencing a source.
    - Cite sources liberally.
    - Do not assume the candidate's gender, keep your evaluation gender-neutral.

    Here is the trait you are evaluating the candidate on:
    {section}
    Here is the description of the trait:
    {trait_description}
    Here is the candidate's name:
    {candidate_full_name}
    Here is the candidate's basic profile:
    {candidate_context}
    Here are the sources about the candidate:
    {source_str}
"""


fit_prompt = """
    Follow these instructions carefully:
    {custom_instructions}

    You are an expert at evaluating candidates for a job.
    You are given a specific job description and a list of ideal candidates for the job.
    You are also given a candidate's name, their basic profile, and a string of sources about the candidate.
    
    Output two values:
    - A score from 0-4 on how well the candidate fits the job given the information provided
    - A string of text outlining your reasoning for the score, without directly referencing the score. This should be no more than 100 words.

    Guidelines:
    - A score of 0 means the candidate is not fit for the job at all - they do not meet any of the requirements
    - A score of 1 means the candidates is likely not fit for the job - they do not meet most of the requirements
    - A score of 2 means the candidate is potentially fit for the job - they check some of the boxes, but may be lacking in other areas
    - A score of 3 means the candidate is a fit for the job - they check most of the boxes and are similar to the ideal profiles
    - A score of 4 means the candidate is an ideal fit for the job - they match the job description and the ideal profiles perfectly
    - Be thoughtful and meticulous in your evaluation, support your claims and carefully analyze the information provided
    - Do not assume the candidate's gender, keep your evaluation gender-neutral.

    Here is the job description:
    {job_description}
    Here is the list of ideal candidates for the job:
    {ideal_profiles}
    Here is the candidate's name:
    {candidate_full_name}
    Here is the candidate's basic profile:
    {candidate_context}
    Here are the sources about the candidate:
    {source_str}
"""
