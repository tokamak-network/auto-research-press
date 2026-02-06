"""Academic categories and journal classification system."""

from typing import Dict, List

# Academic category system - Major fields → Subfields
ACADEMIC_CATEGORIES = {
    "computer_science": {
        "name": "Computer Science",
        "icon": "💻",
        "subfields": {
            "ai_ml": {
                "name": "Artificial Intelligence & Machine Learning",
                "expert_pool": [
                    "deep_learning_expert",
                    "nlp_expert",
                    "computer_vision_expert",
                    "reinforcement_learning_expert"
                ]
            },
            "systems": {
                "name": "Systems, Networks & Distributed Computing",
                "expert_pool": [
                    "distributed_systems_expert",
                    "os_expert",
                    "networking_expert",
                    "database_expert"
                ]
            },
            "theory": {
                "name": "Theory & Algorithms",
                "expert_pool": [
                    "algorithms_expert",
                    "complexity_theory_expert",
                    "formal_methods_expert",
                    "computational_theory_expert"
                ]
            },
            "security": {
                "name": "Security, Cryptography & Privacy",
                "expert_pool": [
                    "cryptography_expert",
                    "network_security_expert",
                    "blockchain_expert",
                    "privacy_expert"
                ]
            },
            "software_eng": {
                "name": "Software Engineering & Programming Languages",
                "expert_pool": [
                    "software_architecture_expert",
                    "programming_languages_expert",
                    "testing_expert",
                    "devops_expert"
                ]
            },
            "hci": {
                "name": "Human-Computer Interaction",
                "expert_pool": [
                    "ux_expert",
                    "interaction_design_expert",
                    "accessibility_expert",
                    "visualization_expert"
                ]
            }
        }
    },

    "engineering": {
        "name": "Engineering & Technology",
        "icon": "⚙️",
        "subfields": {
            "electrical": {
                "name": "Electrical & Electronics Engineering",
                "expert_pool": [
                    "circuits_expert",
                    "signal_processing_expert",
                    "embedded_systems_expert",
                    "power_systems_expert"
                ]
            },
            "mechanical": {
                "name": "Mechanical Engineering",
                "expert_pool": [
                    "thermodynamics_expert",
                    "fluid_mechanics_expert",
                    "materials_expert",
                    "robotics_expert"
                ]
            },
            "civil": {
                "name": "Civil & Structural Engineering",
                "expert_pool": [
                    "structural_analysis_expert",
                    "geotechnical_expert",
                    "transportation_expert",
                    "construction_expert"
                ]
            },
            "materials": {
                "name": "Materials Science",
                "expert_pool": [
                    "nanomaterials_expert",
                    "polymers_expert",
                    "metallurgy_expert",
                    "composites_expert"
                ]
            }
        }
    },

    "natural_sciences": {
        "name": "Natural Sciences",
        "icon": "🔬",
        "subfields": {
            "physics": {
                "name": "Physics & Astronomy",
                "expert_pool": [
                    "quantum_physics_expert",
                    "particle_physics_expert",
                    "astrophysics_expert",
                    "condensed_matter_expert"
                ]
            },
            "chemistry": {
                "name": "Chemistry",
                "expert_pool": [
                    "organic_chemistry_expert",
                    "inorganic_chemistry_expert",
                    "physical_chemistry_expert",
                    "analytical_chemistry_expert"
                ]
            },
            "biology": {
                "name": "Biology & Life Sciences",
                "expert_pool": [
                    "molecular_biology_expert",
                    "genetics_expert",
                    "ecology_expert",
                    "evolutionary_biology_expert"
                ]
            },
            "earth_science": {
                "name": "Earth & Environmental Sciences",
                "expert_pool": [
                    "climate_science_expert",
                    "geology_expert",
                    "oceanography_expert",
                    "environmental_science_expert"
                ]
            },
            "mathematics": {
                "name": "Pure Mathematics",
                "expert_pool": [
                    "number_theory_expert",
                    "topology_expert",
                    "analysis_expert",
                    "algebra_expert"
                ]
            }
        }
    },

    "social_sciences": {
        "name": "Social Sciences",
        "icon": "👥",
        "subfields": {
            "economics": {
                "name": "Economics",
                "expert_pool": [
                    "microeconomics_expert",
                    "macroeconomics_expert",
                    "econometrics_expert",
                    "game_theory_expert"
                ]
            },
            "sociology": {
                "name": "Sociology",
                "expert_pool": [
                    "social_theory_expert",
                    "urban_sociology_expert",
                    "social_networks_expert",
                    "demography_expert"
                ]
            },
            "political_science": {
                "name": "Political Science & International Relations",
                "expert_pool": [
                    "political_theory_expert",
                    "comparative_politics_expert",
                    "international_relations_expert",
                    "public_policy_expert"
                ]
            },
            "psychology": {
                "name": "Psychology & Behavioral Sciences",
                "expert_pool": [
                    "cognitive_psychology_expert",
                    "behavioral_economics_expert",
                    "social_psychology_expert",
                    "neuroscience_expert"
                ]
            },
            "anthropology": {
                "name": "Anthropology",
                "expert_pool": [
                    "cultural_anthropology_expert",
                    "archaeology_expert",
                    "linguistic_anthropology_expert",
                    "biological_anthropology_expert"
                ]
            }
        }
    },

    "humanities": {
        "name": "Humanities",
        "icon": "📚",
        "subfields": {
            "philosophy": {
                "name": "Philosophy",
                "expert_pool": [
                    "ethics_expert",
                    "epistemology_expert",
                    "metaphysics_expert",
                    "logic_expert"
                ]
            },
            "history": {
                "name": "History",
                "expert_pool": [
                    "ancient_history_expert",
                    "modern_history_expert",
                    "historiography_expert",
                    "social_history_expert"
                ]
            },
            "literature": {
                "name": "Literature & Literary Studies",
                "expert_pool": [
                    "literary_theory_expert",
                    "comparative_literature_expert",
                    "poetry_expert",
                    "narrative_studies_expert"
                ]
            },
            "linguistics": {
                "name": "Linguistics",
                "expert_pool": [
                    "syntax_expert",
                    "semantics_expert",
                    "phonology_expert",
                    "sociolinguistics_expert"
                ]
            }
        }
    },

    "business_economics": {
        "name": "Business & Economics",
        "icon": "💼",
        "subfields": {
            "finance": {
                "name": "Finance & Accounting",
                "expert_pool": [
                    "corporate_finance_expert",
                    "financial_markets_expert",
                    "accounting_expert",
                    "risk_management_expert"
                ]
            },
            "management": {
                "name": "Management & Strategy",
                "expert_pool": [
                    "strategic_management_expert",
                    "organizational_behavior_expert",
                    "leadership_expert",
                    "innovation_management_expert"
                ]
            },
            "marketing": {
                "name": "Marketing",
                "expert_pool": [
                    "consumer_behavior_expert",
                    "digital_marketing_expert",
                    "brand_management_expert",
                    "market_research_expert"
                ]
            }
        }
    },

    "medicine_health": {
        "name": "Medicine & Health Sciences",
        "icon": "⚕️",
        "subfields": {
            "clinical": {
                "name": "Clinical Medicine",
                "expert_pool": [
                    "internal_medicine_expert",
                    "surgery_expert",
                    "diagnostics_expert",
                    "therapeutics_expert"
                ]
            },
            "public_health": {
                "name": "Public Health & Epidemiology",
                "expert_pool": [
                    "epidemiology_expert",
                    "health_policy_expert",
                    "disease_prevention_expert",
                    "global_health_expert"
                ]
            },
            "pharmacology": {
                "name": "Pharmacology & Pharmaceutical Sciences",
                "expert_pool": [
                    "drug_discovery_expert",
                    "pharmacokinetics_expert",
                    "clinical_trials_expert",
                    "toxicology_expert"
                ]
            }
        }
    },

    "law_policy": {
        "name": "Law & Public Policy",
        "icon": "⚖️",
        "subfields": {
            "law": {
                "name": "Law & Legal Studies",
                "expert_pool": [
                    "constitutional_law_expert",
                    "international_law_expert",
                    "corporate_law_expert",
                    "legal_theory_expert"
                ]
            },
            "policy": {
                "name": "Public Policy & Administration",
                "expert_pool": [
                    "policy_analysis_expert",
                    "public_administration_expert",
                    "governance_expert",
                    "regulatory_policy_expert"
                ]
            }
        }
    }
}


def get_major_fields() -> List[Dict[str, str]]:
    """Get list of major academic fields."""
    return [
        {
            "id": field_id,
            "name": field_data["name"],
            "icon": field_data["icon"]
        }
        for field_id, field_data in ACADEMIC_CATEGORIES.items()
    ]


def get_subfields(major_field: str) -> List[Dict[str, str]]:
    """Get subfields for a major field."""
    if major_field not in ACADEMIC_CATEGORIES:
        return []

    field_data = ACADEMIC_CATEGORIES[major_field]
    return [
        {
            "id": subfield_id,
            "name": subfield_data["name"]
        }
        for subfield_id, subfield_data in field_data["subfields"].items()
    ]


def get_expert_pool(major_field: str, subfield: str) -> List[str]:
    """Get expert pool for a specific subfield."""
    if major_field not in ACADEMIC_CATEGORIES:
        return []

    field_data = ACADEMIC_CATEGORIES[major_field]
    if subfield not in field_data["subfields"]:
        return []

    return field_data["subfields"][subfield]["expert_pool"]


def get_category_name(major_field: str, subfield: str) -> str:
    """Get full category name."""
    if major_field not in ACADEMIC_CATEGORIES:
        return "Unknown"

    major_name = ACADEMIC_CATEGORIES[major_field]["name"]

    field_data = ACADEMIC_CATEGORIES[major_field]
    if subfield not in field_data["subfields"]:
        return major_name

    subfield_name = field_data["subfields"][subfield]["name"]
    return f"{major_name} → {subfield_name}"
