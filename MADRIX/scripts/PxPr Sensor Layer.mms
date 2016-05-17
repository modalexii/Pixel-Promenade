@scriptname="";
@author="";
@version="";
@description="";

const int CHANNEL_START=0; 
const int CHANNEL_COUNT=100;
const int UNIVERSE=0; // MADRIX GUI "1"
int DmxValues[]; // hold vals read from DMX in

const int SENSOR_ON_MIN=10; // smallest value we treat as "on"
const int SENSOR_ON_MAX=250; // largest we treat as "on"

void InitEffect()
{
	if(IsDMXInEnabled()==0){
		WriteText("DMX in is disabled");
	}
}

void PreRenderEffect()
{
	GetDmxIn(DmxValues,CHANNEL_START,CHANNEL_COUNT,UNIVERSE);
	
	// cAsA
	if(DmxValues[0] < SENSOR_ON_MAX && DmxValues[0] > SENSOR_ON_MIN) {
		LayerSetBlind(0,0); // visible
	}
	else {
		LayerSetBlind(0,1); // hidden
	}
	// cAsB
	if(DmxValues[1] < SENSOR_ON_MAX && DmxValues[1] > SENSOR_ON_MIN) {
		LayerSetBlind(1,0); // visible
	}
	else {
		LayerSetBlind(1,1); // hidden
	}
}

void PostRenderEffect()
{

}

void MatrixSizeChanged()
{
	InitEffect();
}
