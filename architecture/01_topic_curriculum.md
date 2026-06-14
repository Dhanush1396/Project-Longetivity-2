# SOP: Topic Curriculum

## Purpose
Define the full day-by-day topic progression for the longevity study agent.

## Curriculum

### Week 1 — Foundations
| Day | Topic |
|-----|-------|
| 1 | What is Longevity? Lifespan vs Healthspan |
| 2 | The History of Aging Research |
| 3 | The 12 Hallmarks of Aging (López-Otín framework) |
| 4 | How We Measure Biological Age |
| 5 | Genetics vs Lifestyle: What Determines How Long You Live? |
| 6 | Blue Zones — What Centenarians Have in Common |
| 7 | Week 1 Deep Dive: The Science of Healthspan Extension |

### Week 2 — Biology of Aging
| Day | Topic |
|-----|-------|
| 8 | Telomeres and Telomerase |
| 9 | Cellular Senescence — Zombie Cells |
| 10 | Mitochondrial Dysfunction in Aging |
| 11 | Epigenetic Clocks and Aging |
| 12 | Proteostasis — Protein Misfolding and Aging |
| 13 | mTOR, AMPK, and the Nutrient Sensing Pathways |
| 14 | Week 2 Deep Dive: Cellular Mechanisms of Aging |

### Week 3 — Interventions I (Lifestyle)
| Day | Topic |
|-----|-------|
| 15 | Sleep and Longevity — The Science |
| 16 | Exercise as Medicine — VO2 Max and All-Cause Mortality |
| 17 | Strength Training and Muscle Mass in Aging |
| 18 | The Science of Nutrition for Longevity |
| 19 | Protein Intake, mTOR and Longevity Trade-offs |
| 20 | Stress, Cortisol, and Aging |
| 21 | Week 3 Deep Dive: Building a Longevity Lifestyle |

### Week 4 — Interventions II (Metabolic)
| Day | Topic |
|-----|-------|
| 22 | Caloric Restriction and Longevity |
| 23 | Intermittent Fasting — Mechanisms and Evidence |
| 24 | Prolonged Fasting and Autophagy |
| 25 | Hormesis — Why Stress Can Extend Life |
| 26 | Cold Exposure and Heat Stress |
| 27 | The Gut Microbiome and Aging |
| 28 | Week 4 Deep Dive: Metabolic Longevity Levers |

### Week 5 — Pharmacological Interventions
| Day | Topic |
|-----|-------|
| 29 | Rapamycin — The Most Promising Longevity Drug |
| 30 | Metformin as a Longevity Drug |
| 31 | NAD+ Biology and NMN/NR Supplementation |
| 32 | Senolytics — Clearing Zombie Cells |
| 33 | GLP-1 Agonists and Metabolic Longevity |
| 34 | Hormones and Longevity — HRT, Growth Hormone |
| 35 | Week 5 Deep Dive: Drug-Based Longevity Interventions |

### Week 6 — Biomarkers and Testing
| Day | Topic |
|-----|-------|
| 36 | Blood Biomarkers Every Longevity-Focused Person Should Track |
| 37 | Epigenetic Age Testing — Horvath Clock, DunedinPACE |
| 38 | Continuous Glucose Monitoring (CGM) for Longevity |
| 39 | DEXA Scans, VO2 Max Testing, and Functional Fitness |
| 40 | Cardiovascular Risk: ApoB, Lp(a), and Beyond |
| 41 | Cancer Screening and Early Detection |
| 42 | Week 6 Deep Dive: Building Your Longevity Biomarker Panel |

### Week 7 — Frontier Science
| Day | Topic |
|-----|-------|
| 43 | Gene Therapy for Aging |
| 44 | Partial Reprogramming and Yamanaka Factors |
| 45 | Parabiosis and Blood Factors |
| 46 | Stem Cell Therapy |
| 47 | Organ Rejuvenation Technologies |
| 48 | Artificial Intelligence in Longevity Research |
| 49 | Week 7 Deep Dive: The Next 10 Years in Longevity Science |

### Week 8+ — Rotating Deep Dives
After Day 49, cycle through:
- Latest clinical trials
- New research papers (past 30 days)
- Deep dives on specific researchers (Peter Attia, David Sinclair, Morgan Levine, Aubrey de Grey, etc.)
- Protocol analyses (Bryan Johnson's Blueprint, etc.)
- Company spotlights (Altos Labs, Calico, Unity Biotechnology, etc.)

## How the Agent Uses This
- State file `state/day_counter.json` tracks current day number
- Agent maps day number → topic using this curriculum
- Day 50+ uses "rotating" mode — searches for latest research on rotating sub-topics
