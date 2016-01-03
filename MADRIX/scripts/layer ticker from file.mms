@scriptname="layer ticker from file";
@author="Kyle";
@version="MADRIX 2.10";
@description="Pull text form file in to ticker effect";

void InitEffect()
{

}

void PreRenderEffect()
{
string txt;
string file = "C:\temp\src.txt";
SetReadAsyncInterval(file, 5000); // read in to buffer every 5 sec
ReadAsync(file, txt);
SetText(txt);
}

void PostRenderEffect()
{

}

void MatrixSizeChanged()
{
InitEffect();
}
