recommendation_prompt = """
    You are an expert at evaluating candidates for a job.
    You are given a specific job description and a report evaluating specific areas of the candidate.
    Write a recommendation on how good of a fit the candidate is for the job that is based on the information provided.
    This should be a short 2-3 sentence evaluation on how well the candidate fits the job description based on the information provided.
    Here is the job description:
    {job_description}
    Here is the candidate's name:
    {candidate_full_name}
    Here is the report about the candidate:
    {completed_sections}

    When you mention information that you get from a source, please include a citation in your evaluation by citing the number of the source that links to the url in a clickable markdown format.
    For example, if you use information from sources 3 and 7, cite them like this: [3](url), [7](url). 
    Don't include a citation if you are not referencing a source.
"""


trait_evaluation_prompt = """
    You are an expert at evaluating candidates for a job.
    You are given a specific trait that you are evaluating the candidate on, as well as a description of the trait and its type.
    You are also given a string of sources that contain information about the candidate.
    Write an evaluation of the candidate in this specific trait based on the provided information.
    It is possible that there is no information about the candidate in this trait - if this is the case, please mention that no information was found regarding the trait.

    The trait type is: {trait_type}
    {type_specific_instructions}

    Output three values:
    1. A value appropriate for the trait type:
        - For TraitType.BOOLEAN: true/false
        - For TraitType.SCORE: An integer from 0 to 10
    2. A string of text that is the evaluation of the candidate in this specific trait based on the provided information. This should be no more than 100 words.
    3. A string of text that describes what type of trait this is. [TraitType.BOOLEAN, TraitType.SCORE]

    Guidelines:
    - For SCORE traits, don't overscore candidates. Unless they truly have a strong background, don't give them a score above 7. If it's not explicity stated, but can be inferred from previous experience, give them a score that's reasonable based on the information provided.
    - For BOOLEAN traits, only return true if there's clear evidence.
    - In the string of text, when you mention information from a source, include a citation by citing the number of the source that links to the url in clickable markdown format.
    - For example, if you use information from sources 3 and 7, cite them like this: [3](url), [7](url). 
    - Don't include a citation if you are not referencing a source.
    - Cite sources liberally.

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