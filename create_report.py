from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pathlib import Path

ROOT=Path(__file__).resolve().parent
out=ROOT/'report'/'Week4_NLP_Project_Report.docx'
doc=Document()
sec=doc.sections[0]; sec.top_margin=Inches(.7); sec.bottom_margin=Inches(.7); sec.left_margin=Inches(.8); sec.right_margin=Inches(.8)
styles=doc.styles
styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(10)
for s in ['Title','Heading 1','Heading 2']:
    styles[s].font.name='Aptos Display'
styles['Heading 1'].font.color.rgb=RGBColor(31,78,121)
styles['Heading 2'].font.color.rgb=RGBColor(47,84,150)

p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('WEEK 4 NLP PROJECT REPORT'); r.bold=True; r.font.size=Pt(23); r.font.color.rgb=RGBColor(31,78,121)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run('Advanced Analysis and Reporting of Language Trends'); r.bold=True; r.font.size=Pt(16)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
p.add_run('\nSubmitted by\n').bold=True
r=p.add_run('ALISHA MONDAL'); r.bold=True; r.font.size=Pt(14)
p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER
p.add_run('\nProject theme: Evolution of technology-related vocabulary in published English\n')
p.add_run('Techniques: Tokenization, frequency analysis, TF-IDF, LDA, NMF, K-means and trend detection')
doc.add_page_break()

def heading(t,l=1): doc.add_heading(t,level=l)
def para(t): doc.add_paragraph(t)
def bullet(t): doc.add_paragraph(t,style='List Bullet')

heading('Abstract')
para('This project presents a reproducible Natural Language Processing (NLP) workflow for exploring how technology-related language changes over time and how themes can be discovered in a collection of text documents. It combines two public sources for complementary purposes. The 20 Newsgroups dataset is used for document-level text mining, topic modelling and clustering. Google Books Ngram data is used to observe yearly relative frequencies of selected technology-related expressions between 1990 and 2019. The workflow includes text cleaning, tokenization through vectorizers, word-frequency analysis, TF-IDF, Latent Dirichlet Allocation (LDA), Non-negative Matrix Factorization (NMF), K-means clustering and visual reporting. The code fixes random seeds and saves intermediate tables and figures to support repeatability. Since the numerical outputs depend on a successful live data download and model execution, this report describes the analysis design and provides a clear interpretation framework; measured values should be taken from the generated output files rather than guessed.')
heading('1. Introduction')
para('Language changes as communication technologies and social practices change. New terms appear, existing words gain new meanings, and some expressions become more common in public writing. This project studies a focused part of that process: vocabulary associated with digital communication and internet culture. Expressions such as email, website, blog, podcast, hashtag, selfie, emoji and social media provide understandable examples of this shift.')
para('The project also explores the themes found in online discussion text. Topic modelling can reveal groups of words that often occur together, while clustering can group documents with similar word-use patterns. These techniques are exploratory: they help a researcher find patterns, but they do not automatically explain the social meaning of those patterns.')
heading('2. Objectives')
for x in ['Prepare public text data using a consistent preprocessing pipeline.','Measure frequent words and represent documents with numerical text features.','Discover themes using LDA and NMF topic modelling.','Group documents using K-means clustering and inspect cluster sizes.','Track selected vocabulary over time using Google Books Ngram frequencies.','Create clear visualizations and document limitations so that the analysis can be repeated.']: bullet(x)
heading('3. Dataset Selection')
heading('3.1 20 Newsgroups',2)
para('The 20 Newsgroups collection contains approximately 18,000 newsgroup posts arranged across 20 subject categories. Scikit-learn provides a loader that downloads and caches the dataset. The project loads all available subsets and asks the loader to remove headers, footers and quoted replies. This reduces the influence of email-style metadata and repeated quotations, although the removal process is heuristic and may not remove every irrelevant fragment.')
heading('3.2 Google Books Ngram',2)
para('The Google Books Ngram Viewer provides the relative frequency of words and phrases in a book corpus over time. The pipeline requests the English 2019 corpus for eight expressions from 1990 through 2019. The resulting values are relative frequencies, not the number of books or raw occurrences. Google notes that corpus revisions, OCR corrections and language-detection improvements can change historical values.')
heading('3.3 Why two sources are used',2)
para('The two sources are not merged into one dataset because they have different sampling units and purposes. Newsgroup posts are used to discover themes in a discussion corpus. Ngram series are used to observe long-term changes in published books. Using both sources makes it possible to study thematic structure and historical vocabulary trends without pretending that one source represents all language use.')
heading('4. Methodology')
heading('4.1 Data loading and preprocessing',2)
para('The script downloads the 20 Newsgroups data through scikit-learn. Text is converted to lowercase, URLs and non-letter characters are removed, and repeated whitespace is collapsed. Very short cleaned documents are excluded. Vectorizers then perform tokenization and remove common English stop words. This creates a consistent representation for frequency counts and modelling.')
heading('4.2 Frequency analysis',2)
para('CountVectorizer creates a document-term matrix and counts the occurrence of terms across the selected documents. The project saves the most frequent content words to top_word_frequencies.csv and creates a horizontal bar chart. Frequency counts are useful for identifying common vocabulary, but they do not reveal whether a word is meaningful in every context.')
heading('4.3 TF-IDF representation',2)
para('Term Frequency–Inverse Document Frequency (TF-IDF) gives greater weight to terms that are frequent in a document but less common across the full collection. The project uses unigrams and bigrams, limits the vocabulary size and removes very common or very rare terms. This representation is used for NMF and K-means.')
heading('4.4 Topic modelling: LDA and NMF',2)
para('Latent Dirichlet Allocation (LDA) is a probabilistic topic model applied to count vectors. It represents documents as mixtures of topics and topics as distributions over words. Non-negative Matrix Factorization (NMF) factorizes the TF-IDF matrix into document-topic and topic-term components. Both models are configured with six topics for an interpretable first analysis. The six-topic setting is a project choice, not proof that the collection naturally contains exactly six themes. Researchers should compare topic counts and inspect topic coherence in future work.')
heading('4.5 Document clustering',2)
para('K-means partitions TF-IDF document vectors into six groups by minimizing within-cluster distance. The project saves the number of documents assigned to each cluster. A silhouette score is calculated on a bounded sample as a rough measure of separation. Sparse text vectors can be high-dimensional, so this score should be treated as a diagnostic rather than a final quality judgment.')
heading('4.6 Trend detection',2)
para('The Ngram request retrieves annual relative frequencies for the selected expressions from 1990 to 2019, using smoothing level 3. The pipeline plots each expression as a time series. A rising curve indicates a larger share of the corpus containing that expression, not necessarily a rise in everyday spoken use. The time series can be examined for sustained increases, peaks, plateaus and changes in relative ranking.')
heading('5. Implementation and Reproducibility')
para('The complete implementation is stored in src/analyze.py. Dependencies are listed in requirements.txt. A fixed random seed (42) is used for dataset shuffling and model initialization. Running the script downloads the data if needed, creates cleaned data, fits models, requests Ngram data and saves CSV, JSON and PNG outputs. The first run requires an internet connection. The output folder records model settings and the number of documents used so that a reviewer can inspect the actual run.')
para('Recommended command sequence: create a Python virtual environment; install packages with “pip install -r requirements.txt”; then run “python src/analyze.py”. The README file contains Windows PowerShell instructions and an explanation of every output file.')
heading('6. Results and Interpretation')
para('The script generates the evidence needed for this section. To avoid inventing results, no numerical frequency, topic label, cluster score or trend ranking is asserted in this report before the pipeline has been run successfully. After execution, review outputs/run_summary.json, nmf_topics.csv, lda_topics.csv, cluster_sizes.csv, top_word_frequencies.csv and ngram_trends.csv. Use the generated charts to describe the strongest patterns and cite the relevant output file in the final submission.')
heading('6.1 How to interpret the outputs',2)
for x in ['Word frequency chart: identify the most common content words, then explain why frequency alone does not equal importance.','NMF and LDA tables: interpret each topic from its top terms; give a cautious descriptive label and mention ambiguous or overlapping topics.','Cluster sizes: compare the number of documents in each group; inspect example documents before assigning meaning to a cluster.','Ngram trend chart: compare the shape and relative timing of each curve; distinguish sustained growth from short-lived peaks.']: bullet(x)
heading('6.2 Evidence-based reporting checklist',2)
for x in ['Record the exact document count and vocabulary size from run_summary.json.','Quote topic terms directly from the generated topic CSV files.','Describe only trend movements visible in ngram_trends.csv and language_trends.png.','Do not claim that the Newsgroups dataset is representative of all internet users or all modern language.']: bullet(x)
heading('7. Discussion')
para('The combined design demonstrates why different NLP methods answer different questions. Frequency analysis identifies common terms, TF-IDF emphasizes document-specific vocabulary, topic models summarize co-occurring words, clustering groups documents by vector similarity, and Ngram series provide a historical view of selected expressions. No single method is sufficient on its own. Topic models can produce overlapping or difficult-to-name themes, while clusters may reflect vocabulary or dataset artifacts rather than meaningful social groups.')
para('A key challenge is the mismatch between the two sources. Newsgroups is a collection of historical online discussion posts, whereas Google Books represents published books. Differences in audience, genre, publication practices and time coverage mean that a word may become common in online conversation before it becomes common in books. The project therefore treats the datasets as complementary evidence rather than directly comparable measurements.')
heading('8. Limitations')
for x in ['Google Books Ngram covers published books, not private messages, speech or the full social web.','The Ngram corpus and its historical values can change when Google updates OCR, language detection or the corpus.','The 20 Newsgroups dataset is historical and topic-specific; it does not represent current global communication.','Automatic removal of headers, footers and quotations is imperfect.','English-only processing excludes multilingual language change and regional variation.','LDA, NMF and K-means depend on preprocessing choices, topic/cluster counts and random initialization.','A trend in relative frequency does not prove why a term became popular or establish a causal relationship.']: bullet(x)
heading('9. Recommendations and Future Research')
for x in ['Repeat the analysis with recent, licensed social-media or news data that includes reliable timestamps.','Compare multiple corpora, such as books, newspapers, forums and subtitles, while keeping their sampling differences clear.','Test several topic counts and compare topic coherence or human annotation.','Inspect representative documents from each topic and cluster to validate automated labels.','Extend the analysis to multiple languages and compare regional differences.','Use change-point detection or statistical trend tests to identify meaningful shifts rather than relying only on visual inspection.','Document dataset versions, download dates and package versions for stronger reproducibility.']: bullet(x)
heading('10. Conclusion')
para('This project provides a complete and repeatable framework for studying language trends with NLP. It combines traditional text mining, vector-space representations, topic modelling, clustering and historical frequency visualization. Its main strength is the separation of two analytical tasks: discovering themes in a document collection and tracking selected expressions over time in a book corpus. The results should be interpreted carefully because every dataset has limits and every model simplifies language. Running the supplied pipeline and reviewing its generated outputs will provide the empirical values needed for a final evidence-based discussion.')
heading('References')
for x in ['Scikit-learn. “fetch_20newsgroups.” https://scikit-learn.org/stable/modules/generated/sklearn.datasets.fetch_20newsgroups.html','Google Books. “Google Books Ngram Viewer: Information and Release Notes.” https://books.google.com/ngrams/info','Scikit-learn. “Topic extraction with Non-negative Matrix Factorization and Latent Dirichlet Allocation.” https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html']:
    bullet(x)
heading('Appendix: Files produced by the pipeline')
for x in ['cleaned_newsgroups_sample.csv — cleaned text and source category.','top_word_frequencies.csv — token counts.','nmf_topics.csv and lda_topics.csv — topic terms and NMF document assignments.','cluster_sizes.csv — document count per K-means cluster.','ngram_trends.csv — yearly relative frequency for each phrase.','run_summary.json — run configuration and diagnostic values.','word_frequency.png, topic_distribution.png and language_trends.png — generated visualizations.']: bullet(x)

# Footer
for section in doc.sections:
    f=section.footer.paragraphs[0]; f.alignment=WD_ALIGN_PARAGRAPH.CENTER
    f.add_run('Week 4 NLP Project | Alisha Mondal')

doc.save(out)
print(out)
