# ELEVATE X AI — FEATURE 1: ERROR ANALYSIS & 100-SAMPLE INSPECTION REPORT

## 1. Summary of 100 Sample Audits

- **Total Audit Samples:** 100
- **Offset Invariant Verified:** `217` spans verified with `input_text[start:end] == extracted_skill` (100% boundary integrity, 0 slicing violations).
- **Exact Matches (TP):** `179`
- **Partial Overlaps:** `38`
- **False Positives (FP):** `38`
- **False Negatives (FN):** `37`

## 2. Qualitative Error Taxonomy

### A. Compound Action & Auxiliary Verb Boundary Drift
- **Occurrence:** In Hinglish and Hindi, compound verbal predicates (e.g., *fitting karna*, *welding marte hain*, *plumbing check kiya*) occasionally have the auxiliary verb (*karna*, *kiya*) excluded from the gold annotation but included by the token tagger, causing a partial overlap match.
- **Mitigation:** Post-processing regex filter to strip trailing auxiliary light verbs (*karna*, *hona*, *dena*) from extracted skill spans.

### B. Code-Switching Transliteration Ambiguity
- **Occurrence:** In Romanized Hindi (`hi_latn`), varied phonetic spellings (e.g. *dhaga/dhaaga*, *choli/choliya*, *tanki/tankee*) lead to slight drop in exact span recall compared to Devanagari.
- **Mitigation:** Subword byte-level BPE in XLM-RoBERTa handles word pieces, but character-level phonetic normalization will further boost robustness.

## 3. Representative Sample Predictions (Audit Subset)

#### Record `MOCK-TRD-01-00087` (Tailor and Garment Worker — `hindi`)
- **Text:** *"सुरक्षा को ध्यान में रखकर हम ओवरलॉक सिलाई करते हैं और समय-समय पर ग्राहक का नाप लेना।"*
- **Gold Spans:** `ओवरलॉक सिलाई` (technical_tactile), `ग्राहक का नाप लेना` (measurement_planning)
- **Predicted Spans:** `ओवरलॉक सिलाई`, `ग्राहक का नाप लेना।`
- **Exact Matches:** `ओवरलॉक सिलाई`

#### Record `MOCK-TRD-01-00032` (Tailor and Garment Worker — `hindi`)
- **Text:** *"जब ग्राहक साइट पर बुलाते हैं तो पहले बकरम चिपकाना और कॉलर बनाना करते हैं और फिर ओवरलॉक सिलाई।"*
- **Gold Spans:** `बकरम चिपकाना और कॉलर बनाना` (technical_tactile), `ओवरलॉक सिलाई` (technical_tactile)
- **Predicted Spans:** `बकरम चिपकाना और कॉलर बनाना`, `ओवरलॉक सिलाई।`
- **Exact Matches:** `बकरम चिपकाना और कॉलर बनाना`

#### Record `MOCK-TRD-01-00082` (Tailor and Garment Worker — `hindi`)
- **Text:** *"दैनिक रूटीन में सबसे पहले फिटिंग अल्टरेशन करना की तैयारी करते हैं, उसके बाद नीडल गार्ड सेफ्टी चेक और फिर सिलाई मशीन चलाना की जांच करते हैं।"*
- **Gold Spans:** `फिटिंग अल्टरेशन करना` (troubleshooting_repair), `नीडल गार्ड सेफ्टी चेक` (safety_compliance), `सिलाई मशीन चलाना` (tool_operation)
- **Predicted Spans:** `फिटिंग अल्टरेशन करना`, `नीडल गार्ड सेफ्टी चेक`, `सिलाई मशीन चलाना`
- **Exact Matches:** `फिटिंग अल्टरेशन करना`, `नीडल गार्ड सेफ्टी चेक`, `सिलाई मशीन चलाना`

#### Record `MOCK-TRD-01-00168` (Tailor and Garment Worker — `roman_hindi`)
- **Text:** *"Customer ke hisaab se pehle customer se design baat-chit karte hain aur delivery se pehle kapde ki cutting check karte hain."*
- **Gold Spans:** `customer se design baat-chit` (client_communication), `kapde ki cutting` (measurement_planning)
- **Predicted Spans:** `customer se design baat-chit`, `kapde ki cutting`
- **Exact Matches:** `kapde ki cutting`, `customer se design baat-chit`

#### Record `MOCK-TRD-01-00177` (Tailor and Garment Worker — `roman_hindi`)
- **Text:** *"Mera main kaam overlock silai ka hai lekin project par katori blouse dart silai bhi handle karta hu."*
- **Gold Spans:** `overlock silai` (technical_tactile), `katori blouse dart silai` (technical_tactile)
- **Predicted Spans:** `overlock silai`, `katori blouse dart silai`
- **Exact Matches:** `katori blouse dart silai`, `overlock silai`

#### Record `MOCK-TRD-01-00252` (Tailor and Garment Worker — `hinglish`)
- **Text:** *"Safety protocol follow karte huye body measurement taking compulsory hai aur alongside customer design consultation karte hain."*
- **Gold Spans:** `body measurement taking` (measurement_planning), `customer design consultation` (client_communication)
- **Predicted Spans:** `body measurement taking`, `customer design consultation`
- **Exact Matches:** `customer design consultation`, `body measurement taking`

#### Record `MOCK-TRD-01-00266` (Tailor and Garment Worker — `hinglish`)
- **Text:** *"Service quality maintain karne ke liye pehle fabric cutting and pattern marking and handover se pehle lockstitch machine stitching inspect karte hain."*
- **Gold Spans:** `fabric cutting and pattern marking` (measurement_planning), `lockstitch machine stitching` (tool_operation)
- **Predicted Spans:** `fabric cutting and pattern marking`, `lockstitch machine stitching`
- **Exact Matches:** `fabric cutting and pattern marking`, `lockstitch machine stitching`

#### Record `MOCK-TRD-01-00333` (Tailor and Garment Worker — `english`)
- **Text:** *"My daily workshop duties include checking machine finger safety guards and conducting fusible collar stiffener attachment when required."*
- **Gold Spans:** `checking machine finger safety guards` (safety_compliance), `fusible collar stiffener attachment` (technical_tactile)
- **Predicted Spans:** `checking machine finger safety guards`, `fusible collar stiffener attachment`
- **Exact Matches:** `checking machine finger safety guards`, `fusible collar stiffener attachment`

#### Record `MOCK-TRD-01-00319` (Tailor and Garment Worker — `english`)
- **Text:** *"My core technical competence is fusible collar stiffener attachment, with extensive project experience in garment alteration and seam restructuring."*
- **Gold Spans:** `fusible collar stiffener attachment` (technical_tactile), `garment alteration and seam restructuring` (troubleshooting_repair)
- **Predicted Spans:** `fusible collar stiffener attachment,`, `garment alteration and seam restructuring.`
- **Exact Matches:** *None*

#### Record `MOCK-TRD-01-00491` (Tailor and Garment Worker — `mixed`)
- **Text:** *"Main workshop me tailor chalk से fabric cutting karta hu aur customer requirement par customer requirement consultation execute karta hu."*
- **Gold Spans:** `tailor chalk से fabric cutting` (measurement_planning), `customer requirement consultation` (client_communication)
- **Predicted Spans:** `tailor chalk से fabric cutting`, `customer requirement consultation`
- **Exact Matches:** `tailor chalk से fabric cutting`, `customer requirement consultation`

