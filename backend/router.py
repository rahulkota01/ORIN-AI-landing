"""
Orin - Smart Query Classifier / Router
Routes user queries to the appropriate AI model based on content analysis.
"""

import re

# Casual patterns — greetings, small talk, thanks
CASUAL_PATTERNS = [
    r"\b(hi|hello|hey|hola|namaste|sup|yo)\b",
    r"\b(how are you|how's it going|what's up|howdy)\b",
    r"\b(thanks|thank you|thankyou|thx|ty|dhanyavaad|shukriya)\b",
    r"\b(good morning|good evening|good night|good afternoon)\b",
    r"\b(bye|goodbye|see you|take care|later)\b",
    r"\b(ok|okay|cool|nice|great|awesome|got it)\b",
    r"\b(who are you|what are you|your name|tell me about yourself)\b",
]

# Complex science keywords — triggers Claude
COMPLEX_SCIENCE_KEYWORDS = [
    # Drug discovery & pharmacology
    r"\b(drug discovery|drug design|pharmacokinetics|pharmacodynamics)\b",
    r"\b(admet|adme|bioavailability|half[ -]life|clearance)\b",
    r"\b(ic50|ec50|ki value|dose[ -]response|sar|qsar)\b",
    r"\b(clinical trial|phase [1-4]|fda approval|ema)\b",
    r"\b(mechanism of action|moa|target identification)\b",
    # Molecular biology & biochemistry
    r"\b(molecular docking|molecular dynamics|binding affinity)\b",
    r"\b(protein folding|protein structure|homology modeling)\b",
    r"\b(gene expression|transcription factor|epigenetics)\b",
    r"\b(crispr|cas9|gene editing|gene therapy)\b",
    r"\b(signal transduction|pathway analysis|metabolic pathway)\b",
    # Genomics & computational biology
    r"\b(genomics|proteomics|metabolomics|transcriptomics)\b",
    r"\b(sequence alignment|blast|phylogenetic)\b",
    r"\b(smiles|inchi|molecular formula|chemical structure)\b",
    r"\b(docking score|binding energy|free energy)\b",
    # Research-oriented
    r"\b(research paper|literature review|systematic review|meta[ -]analysis)\b",
    r"\b(hypothesis|methodology|experimental design)\b",
    r"\b(p[ -]value|statistical significance|confidence interval)\b",
    r"\b(formulation|excipient|bioequivalence|dissolution)\b",
]

# Simple factual science keywords — triggers Groq for fast answers
SIMPLE_SCIENCE_KEYWORDS = [
    r"\b(what is|what are|define|definition of|meaning of)\b",
    r"\b(explain|describe|tell me about|overview of)\b",
    r"\b(function of|role of|importance of|purpose of)\b",
    r"\b(difference between|compare|vs|versus)\b",
    r"\b(types of|classification of|categories of)\b",
    r"\b(example of|examples of|list of)\b",
    r"\b(structure of|composition of|components of)\b",
    r"\b(uses of|applications of|benefits of)\b",
    # Basic science terms
    r"\b(cell|organ|tissue|enzyme|hormone|vitamin|mineral)\b",
    r"\b(bacteria|virus|fungus|parasite|pathogen)\b",
    r"\b(dna|rna|amino acid|protein|lipid|carbohydrate)\b",
    r"\b(mitosis|meiosis|photosynthesis|respiration)\b",
    r"\b(antibiotic|vaccine|drug|medicine|tablet|capsule)\b",
    r"\b(pharmacology|biology|chemistry|biochemistry)\b",
]


def classify_query(message: str, has_image: bool = False) -> tuple[str, str]:
    """
    Classify the user's query and determine which AI model to route it to.

    Returns:
        tuple: (query_type, model_provider)
            - query_type: casual / science / research / drug / image
            - model_provider: groq / claude / gemini
    """
    lower_message = message.lower().strip()

    # Rule 1: If query contains an image → Gemini
    if has_image:
        return ("image", "gemini")

    # Rule 2: Check for casual patterns
    for pattern in CASUAL_PATTERNS:
        if re.search(pattern, lower_message):
            # Make sure it's primarily casual (short message)
            if len(lower_message.split()) <= 10:
                return ("casual", "groq")

    # Rule 3: Check for complex science / research / drug discovery → Claude
    for pattern in COMPLEX_SCIENCE_KEYWORDS:
        if re.search(pattern, lower_message, re.IGNORECASE):
            # Determine sub-type
            if re.search(
                r"\b(drug|molecule|compound|smiles|docking|admet|formulation)\b",
                lower_message,
                re.IGNORECASE,
            ):
                return ("drug", "claude")
            if re.search(
                r"\b(research|paper|literature|review|study|journal)\b",
                lower_message,
                re.IGNORECASE,
            ):
                return ("research", "claude")
            return ("science", "claude")

    # Rule 4: Check for simple factual science → Groq (fast)
    for pattern in SIMPLE_SCIENCE_KEYWORDS:
        if re.search(pattern, lower_message, re.IGNORECASE):
            return ("science", "groq")

    # Rule 5: Default fallback → Groq
    return ("casual", "groq")
