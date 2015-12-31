@scriptname="";
@author="";
@version="";
@description="";

void InitEffect() { }

void PreRenderEffect() {

	string txt;
	string file = "C:\temp\src.txt";
	SetReadAsyncInterval(file, 10000); // read in to buffer every 10 sec
	ReadAsync(file, txt);
	
	// location of text for ticker
	int txtPipeline = STORAGE_RIGHT;
	int txtStorage = 1; // script counts from 0, so use GUI # - 1
	int txtStoragePlace = 256; // script and GUI count from 1
	int txtTransition = WITH_AUTOFADE; // WITH_ or WITHOUT_
	
	if(txt) {
		CuelistStop();
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
