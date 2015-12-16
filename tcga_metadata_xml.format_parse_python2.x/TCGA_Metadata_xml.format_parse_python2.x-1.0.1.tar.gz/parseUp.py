import bs4

openUp = open("/Users/brucewilliam/Desktop/metadata.xml", "r")
parseUp = bs4.BeautifulSoup(openUp, "xml")

newSet = open("/Users/brucewilliam/Desktop/Collection/Liver_Hepatocellular_Carcinoma.txt", "w")
newSet.write("\t".join(["ParticipantID", "AnalysisID", "Disease", "SampleID", "AnalyteCode", "SampleType", "Library", "Platform", "Design", "LibrarySelect"]) + "\n")

for result in parseUp.findAll(name="Result"):
	participantid = result.find("participant_id").text
	analyid = result.find("analysis_id").text
	disease = result.find("disease_abbr").text
	sampleid = result.find("sample_id").text
	analyte = result.find("analyte_code").text
	sampletype = result.find("sample_type").text
	librarystra = result.find("library_strategy").text
	platf = result.find("platform").text
	design = result.find("DESIGN_DESCRIPTION").text
	libsele = result.find("LIBRARY_SELECTION").text
	newSet.write("\t".join([participantid, analyid, disease, sampleid, analyte, sampletype, librarystra, platf, design, libsele]) + "\n")

openUp.close()
newSet.close()
