# ELEVATE X AI — FEATURE 1: MODEL ERROR ANALYSIS & QUALITATIVE EVALUATION

**Evaluation Date**: `2026-11-15 07:00:08 UTC`  
**Evaluated Checkpoint**: `best_skillspan_model`  

## 1. Quantitative Error Taxonomy

| Error Category | Count | Percentage of Gold/Pred | Description |
| :--- | :--- | :--- | :--- |
| **Exact True Positives** | `322` | `29.5%` of gold | Both start and end character offsets matched exactly |
| **Boundary Discrepancies** | `451` | `41.3%` of gold | Skill concept identified, but boundary differed by 1-2 words/tokens |
| **Pure False Positives** | `759` | `49.5%` of pred | Extracted entity not annotated as a skill in gold standard |
| **Pure False Negatives** | `318` | `29.1%` of gold | Gold skill entity completely missed by the model |

## 2. Root Cause Analysis of Dominant Error Modes

### Error Mode 1: Boundary Granularity (Compound Skill Phrases)
- **Pattern**: Gold annotates `[lead software development teams]`, while model extracts `[software development]`.
- **Analysis**: In skill extraction, annotator subjectivity in SkillSpan often fluctuates between minimal verb phrases and full predicate phrases. The model favors modular, actionable skill units, which lowers strict Exact Span F1 while Partial Overlap F1 captures the true functional capability.

### Error Mode 2: Multi-Word Domain Tools & Niche Frameworks
- **Pattern**: Gold annotates `[React Native]`, model predicts `[React]` as B-SKILL and misses `Native`.
- **Analysis**: Subword segmentation on hyphenated or multi-capitalized proprietary frameworks can split tokens across rare BPE boundaries.

### Error Mode 3: Domain False Positives (Job Titles vs Skills)
- **Pattern**: Gold leaves `Senior Full Stack Engineer` as `O`, model predicts `Full Stack Engineer` as skill.
- **Analysis**: Syntactic overlap between occupational titles and skill proficiencies causes spurious skill detections in sentence opening positions.

## 3. Qualitative Inspection: 50 Test Sentence Predictions

The table below inspects 50 test sentences. Every span verified: `assert text[start:end] == extracted_skill`.

| ID | Sentence Excerpt | Gold Skills | Predicted Skills | Match Assessment |
| :--- | :--- | :--- | :--- | :--- |
| `1` | Full Stack Software Engineer - Java / JavaScript | *(None)* | *(None)* | **True Negative (No Skills)** |
| `2` | <ORGANIZATION> <ORGANIZATION> <ORGANIZATION> <ORGANIZATION> . | *(None)* | *(None)* | **True Negative (No Skills)** |
| `3` | <ADDRESS> <ADDRESS> <LOCATION> - <LOCATION> | *(None)* | *(None)* | **True Negative (No Skills)** |
| `4` | Date posted: 2021-03-04 | *(None)* | *(None)* | **True Negative (No Skills)** |
| `5` | Likes: 0 Dislikes: 0 Love: 0 | *(None)* | *(None)* | **True Negative (No Skills)** |
| `6` | Salary: <SALARY> | *(None)* | *(None)* | **True Negative (No Skills)** |
| `7` | Job type: FULL_TIME | *(None)* | *(None)* | **True Negative (No Skills)** |
| `8` | Experience level: <EXPERIENCE> | *(None)* | *(None)* | **True Negative (No Skills)** |
| `9` | Industry: <INDUSTRY> | *(None)* | *(None)* | **True Negative (No Skills)** |
| `10` | Company size: <SIZE> | *(None)* | *(None)* | **True Negative (No Skills)** |
| `11` | Company type: <COMPANY_TYPE> | *(None)* | *(None)* | **True Negative (No Skills)** |
| `12` | Technologies: | *(None)* | *(None)* | **True Negative (No Skills)** |
| `13` | javascript reactjs java | *(None)* | *(None)* | **True Negative (No Skills)** |
| `14` | Job description: | *(None)* | *(None)* | **True Negative (No Skills)** |
| `15` | Job type: | *(None)* | *(None)* | **True Negative (No Skills)** |
| `16` | Full-time | *(None)* | *(None)* | **True Negative (No Skills)** |
| `17` | Role: | *(None)* | *(None)* | **True Negative (No Skills)** |
| `18` | Full Stack Developer | *(None)* | *(None)* | **True Negative (No Skills)** |
| `19` | Technologies | *(None)* | *(None)* | **True Negative (No Skills)** |
| `20` | javascript reactjs java | *(None)* | *(None)* | **True Negative (No Skills)** |
| `21` | Job description | *(None)* | *(None)* | **True Negative (No Skills)** |
| `22` | As a member of our <ORGANIZATION> <ORGANIZATION> <ORGANIZATION> we look first and forem... | solving business problems [128:153] | solving business problems through innovation and engineering practices [128:198] | **Boundary Overlap** |
| `23` | You'll be required to apply your depth of knowledge and expertise to all aspects of the... | apply your depth of knowledge and expertise [22:65]<br>partner continuously with your many stakeholders [130:178]<br>stay focused on common goals [199:227] | apply your depth of knowledge and expertise to all aspects [22:80]<br>the software development [84:108]<br>partner continuously with your many stakeholders on a daily basis [130:195]<br>stay focused on common goals [199:227] | **Partial / Mixed Match** |
| `24` | We embrace a culture of experimentation and constantly strive for improvement and learn... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `25` | You'll work in a collaborative trusting thought-provoking environment-one that encourag... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `26` | This opportunity requires a highly motivated candidate to work in a small and talented ... | motivated [35:44]<br>deliver of a next-generation analytics products [125:172] | highly [28:34]<br>motivated [35:44]<br>work [58:62]<br>talented [78:86]<br>deliver of a next-generation analytics products [125:172] | **Partial / Mixed Match** |
| `27` | The analytics solutions will be a commercial business in its own right so a heavy empha... | *(None)* | building technology [94:113] | **False Positive** |
| `28` | This framework is at an early stage of development which offers an opportunity for an e... | *(None)* | experienced developer [86:107]<br>help [111:115]<br>shape the key components of the product and [116:159]<br>create commercial opportunities for a new business [160:210] | **False Positive** |
| `29` | You will partner primarily with fellow technologists from across lines of business Prod... | *(None)* | partner [9:16]<br>with [27:31]<br>build a modern and comprehensive API [132:168]<br>clients [178:185]<br>easily [189:195]<br>define and compute analytics [196:224] | **False Positive** |
| `30` | * • BS/BA degree or equivalent experience | *(None)* | *(None)* | **True Negative (No Skills)** |
| `31` | * • Advanced knowledge of application data and infrastructure architecture disciplines | *(None)* | *(None)* | **True Negative (No Skills)** |
| `32` | * • Understanding of architecture and design across all systems | *(None)* | *(None)* | **True Negative (No Skills)** |
| `33` | * • Working proficiency in developmental toolsets | developmental toolsets [27:49] | *(None)* | **False Negative** |
| `34` | * • Knowledge of industry-wide technology strategies and best practices | *(None)* | *(None)* | **True Negative (No Skills)** |
| `35` | * • Ability to work in large collaborative teams to achieve organizational goals and pa... | work in large collaborative teams [15:48]<br>achieve organizational goals [52:80]<br>building an innovative culture [102:132] | work in large collaborative teams [15:48]<br>achieve organizational goals [52:80]<br>passionate [85:95]<br>building an innovative culture [102:132] | **Partial / Mixed Match** |
| `36` | * • Proficiency in one or more modern programming languages - Java and Javascript prefe... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `37` | * • Understanding of software skills such as business analysis development maintenance ... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `38` | * • In-depth HTML5 / JavaScript | *(None)* | *(None)* | **True Negative (No Skills)** |
| `39` | * • Competent with developing multithreaded scalable concurrent applications . | developing multithreaded scalable concurrent applications [19:76] | developing multithreaded scalable concurrent applications [19:76] | **Exact Match** |
| `40` | * • Node JS ( server side and tooling ) * • React or similar view framework | *(None)* | *(None)* | **True Negative (No Skills)** |
| `41` | <ORGANIZATION> <ORGANIZATION> <ORGANIZATION> is a global leader in financial services p... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `42` | Our first-class business in a first-class way approach to serving clients drives everyt... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `43` | We strive to build trusted long-term partnerships to help our clients achieve their bus... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `44` | We recognize that our people are our strength and the diverse talents they bring to our... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `45` | We are an equal opportunity employer and place a high value on diversity and inclusion ... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `46` | We do not discriminate on the basis of any protected attribute including race religion ... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `47` | In accordance with applicable law we make reasonable accommodations for applicants' and... | *(None)* | *(None)* | **True Negative (No Skills)** |
| `48` | Job benefits: - | *(None)* | *(None)* | **True Negative (No Skills)** |
| `49` | Company description: | *(None)* | *(None)* | **True Negative (No Skills)** |
| `50` | <DESCRIPTION> | *(None)* | *(None)* | **True Negative (No Skills)** |
