# ELEVATE X AI — MULTILINGUAL VOCABULARY & LANGUAGE COVERAGE REPORT
**Report Timestamp**: 2026-11-14 21:00:38  
**Target Architecture**: Devanagari Hindi, Romanized Hinglish, Trade English Loanwords  

---

## 1. Executive Summary
- **Curated Trade Terminology Entries**: **24 key vernacular terms**
- **Core Vocational Action Verbs**: **7 procedural verbs**
- **Covered Linguistic Scripts**: Devanagari (Hindi) and Latin (Phonetic Hinglish & English)
- **Preservation Policy**: 100% unstemmed verbatim text retention; zero forced English translation

## 2. Exemplary Vernacular Trade Terms by Occupation
| ID | Trade Domain | Devanagari Script | Romanized Hinglish | Standard English Concept | Common Phonetic Variants |
|---|---|---|---|---|---|
| `TRM-001` | **Tailoring** | सिलाई | `silai` | sewing / stitching | seelai, silaai |
| `TRM-002` | **Tailoring** | बकरम | `bakram` | fusible canvas interlining | bukram, buckram |
| `TRM-003` | **Tailoring** | कटोरी कटिंग | `katora cutting` | contoured blouse cup pattern | katori cut, choli cut |
| `TRM-004` | **Tailoring** | ओवरलॉक | `overlock` | overedge serging | interlock, overlok |
| `TRM-005` | **Electrical** | झिरी | `jhirri` | wall conduit chasing groove | jhiri, jheeri |
| `TRM-006` | **Electrical** | अर्थिंग | `earthing` | electrical ground electrode | arthing, ground |
| `TRM-007` | **Electrical** | न्यूट्रल-फेज | `neutral-phase` | AC mains live and neutral polarity | neutral phase, line neutral |
| `TRM-008` | **Plumbing** | सॉल्वेंट | `solvent` | CPVC/UPVC chemical cement | solvant, salvent |
| `TRM-009` | **Plumbing** | चूड़ी | `chudi` | external pipe screw threads | choori, churi |
| `TRM-010` | **Plumbing** | डायवर्टर | `diverter` | concealed shower mixer valve | divertor, mixer |
| `TRM-011` | **Mechanic** | टैपेट | `tappet` | engine valve rocker clearance | tapet, tepet |
| `TRM-012` | **Mechanic** | क्लच प्लेट | `clutch plate` | friction clutch disk | clutch plate, kalach |
| `TRM-013` | **Carpentry** | रंदा | `randa` | wood hand planer | randha, randaa |
| `TRM-014` | **Carpentry** | सनमाइका | `sunmica` | decorative high-pressure laminate | sanmika, laminate |
| `TRM-015` | **Welding** | चिप्पिंग | `chipping` | weld slag chipping hammer action | chipin, slag safai |
| `TRM-016` | **Welding** | टांका | `taka` | tack weld bead | taanka, tack |
| `TRM-017` | **Masonry** | साहुल | `sahul` | mason's brass plumb bob | sahool, plumb bob |
| `TRM-018` | **Masonry** | घोंटाई | `ghoontai` | neat cement float waterproofing | ghontai, ghotai |
| `TRM-019` | **Painting** | रेगमार | `regmar` | abrasive silicon carbide sandpaper | regmaal, sandpaper |
| `TRM-020` | **Painting** | पुट्टी पत्ती | `putty patti` | steel wall putty knife blade | patti, patra |
| `TRM-021` | **Agriculture** | ड्रिप लाइन | `drip line` | micro-irrigation lateral tubing | drip pipe, lateral line |
| `TRM-022` | **Agriculture** | वेंचुरी | `venturi` | differential fertilizer injector | venchury, venturi dosing |
| `TRM-023` | **Mobile Repair** | सीसी पिन | `CC pin` | charging connector port pin | charging pin, jack |
| `TRM-024` | **Mobile Repair** | जंपर | `jumper` | fine micro-wire PCB track bypass | jampar, jumper wire |

## 3. High-Frequency Action Verbs in Informal Trade Utterances
| Verb ID | Devanagari | Hinglish | English Meaning | Primary Trade Contexts |
|---|---|---|---|---|
| `VRB-001` | काटना | `kaatna` | cutting / slicing / chasing | fabric, pipe, wall conduit, metal plate |
| `VRB-002` | सिलना | `silna` | stitching / seaming | garments, curtains, canvas |
| `VRB-003` | चिपकाना | `chipkana` | gluing / bonding / fusing | sunmica, bakram, display folders |
| `VRB-004` | खींचना | `kheenchna` | skimming / pulling | putty application, wire pulling in conduits |
| `VRB-005` | घिसना | `ghisana` | sanding / abrading / grinding | regmar sanding, angle grinder beveling |
| `VRB-006` | जोड़ना | `jorna` | jointing / coupling / wiring | pipe solvent joints, MCB terminations, implement hitching |
| `VRB-007` | जांचना | `jaanchana` | inspecting / measuring / diagnosing | multimeter testing, feeler gauge, plumb bob |

## 4. NLP Tokenization & Script Handling Guidelines
1. **Phonetic Script Code-Switching**: Spoken trade descriptions frequently mix scripts (*'Main 1.5 sq mm wire conduit mein daalta hu'*). Tokenizers must handle sub-word splits on numbers and gauge units.
2. **Compound Conjunctive Verbs**: Actions often appear as verb + helper pairs (*'silai karta hu'*, *'fitting karta hu'*, *'check karta hu'*). Span extraction must encompass the full functional verb clause.
3. **Zero Translation Distortion**: Models must be evaluated on verbatim strings without English normalization.
