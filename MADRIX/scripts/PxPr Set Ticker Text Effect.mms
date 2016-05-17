@scriptname="PxPr Set Ticker Text Effect";
@author="Kyle";
@version="MADRIX 2.10";
@description="Pull text form file in to ticker effect and set BPM";

float TEXT_WIDTH;

void InitEffect()
{

}

void PreRenderEffect()
{
	string txt;
	string file = "C:\ProgramData\MADRIX\ticker_src.txt";
	SetReadAsyncInterval(file, 5000); // read in to buffer every 5 sec
	ReadAsync(file, txt);
	WriteText(txt);
	SetText(txt);
	
	// set BPM relative to width of text for consistant scroll spped
	TEXT_WIDTH = GetImagePixelWidth();
	SetBpm( 66.66 * pow(0.999, TEXT_WIDTH) + 7 );
	WriteText( GetFontWidth() );
	SetFontWidth(7);
	SetFontHeight(100);
	SetFontWeight(550);
}

void PostRenderEffect()
{

}

void MatrixSizeChanged()
{
InitEffect();
}
