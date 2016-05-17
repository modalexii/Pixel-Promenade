@scriptname="master cue to ticker governor";
@author="Kyle";
@version="MADRIX 2.10";
@description="Fade main output to ticker when text source file is not empty";

void InitEffect() { }

void PreRenderEffect() {

	string txt;
	string file = "C:\ProgramData\MADRIX\ticker_src.txt";
	SetReadAsyncInterval(file, 10000); // read in to buffer every 10 sec
	ReadAsync(file, txt);
	
	// location of text for ticker
	int txtPipeline = STORAGE_RIGHT;
	int txtStorage = 1; // MADRIX GUI "2"
	int txtStoragePlace = 1; // MADRIX GUI "2"
	int txtTransition = WITH_AUTOFADE; // WITH_ or WITHOUT_
	
	if(txt) {
		CuelistStop();
		SetFadeType(CROSSFADE); // or else current settig from cue will be used
		SetFadeTime(10); // or else current settig from cue will be used
		SetStorage(txtPipeline, txtStorage);
		SetStoragePlace(txtPipeline, txtStoragePlace, txtTransition);
	} else {
		CuelistPlay();
	}

}

void PostRenderEffect() { }

void MatrixSizeChanged() {
	InitEffect();
}
