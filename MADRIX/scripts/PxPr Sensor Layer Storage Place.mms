@scriptname="PxPr Sensor Layer Storage Place";
@author="";
@version="";
@description="";

const int CHANNEL_START=0; 
const int CHANNEL_COUNT=100;
const int UNIVERSE=0; // MADRIX GUI "1"
int DmxValues[]; // hold vals read from DMX in

const int SENSOR_ON_MIN=10; // smallest value we treat as "on"
const int SENSOR_ON_MAX=110; // largest we treat as "on"

const int BASE_LAYERS=1; // number of layers under the sensor effects

void InitEffect()
{
	if(IsDmxInEnabled()==0){
		WriteText("DMX in is disabled");
	}
}

void PreRenderEffect()
{
	GetDmxIn(DmxValues,CHANNEL_START,CHANNEL_COUNT,UNIVERSE);
	
	// cAsA
	if(DmxValues[0] < SENSOR_ON_MAX && DmxValues[0] > SENSOR_ON_MIN) {
		WriteText("cAsA: proximity");
		LayerSetBlind(0+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(0+BASE_LAYERS,1); // hidden
	}
	// cAsB
	if(DmxValues[1] < SENSOR_ON_MAX && DmxValues[1] > SENSOR_ON_MIN) {
		WriteText("cAsB: proximity");
		LayerSetBlind(1+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(1+BASE_LAYERS,1); // hidden
	}
	
	// cBsA
	if(DmxValues[8] < SENSOR_ON_MAX && DmxValues[8] > SENSOR_ON_MIN) {
		WriteText("cBsA: proximity");
		LayerSetBlind(2+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(2+BASE_LAYERS,1); // hidden
	}
	// cBsB
	if(DmxValues[9] < SENSOR_ON_MAX && DmxValues[9] > SENSOR_ON_MIN) {
		WriteText("cBsB: proximity");
		LayerSetBlind(3+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(3+BASE_LAYERS,1); // hidden
	}
	
	// cCsA
	if(DmxValues[16] < SENSOR_ON_MAX && DmxValues[16] > SENSOR_ON_MIN) {
		WriteText("cCsA: proximity");
		LayerSetBlind(4+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(4+BASE_LAYERS,1); // hidden
	}
	// cCsB
	if(DmxValues[17] < SENSOR_ON_MAX && DmxValues[17] > SENSOR_ON_MIN) {
		WriteText("cCsB: proximity");
		LayerSetBlind(5+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(5+BASE_LAYERS,1); // hidden
	}
	
	// cDsA
	if(DmxValues[24] < SENSOR_ON_MAX && DmxValues[24] > SENSOR_ON_MIN) {
		WriteText("cDsA: proximity");
		LayerSetBlind(6+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(6+BASE_LAYERS,1); // hidden
	}
	// cDsB
	if(DmxValues[25] < SENSOR_ON_MAX && DmxValues[25] > SENSOR_ON_MIN) {
		WriteText("cDsB: proximity");
		LayerSetBlind(7+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(7+BASE_LAYERS,1); // hidden
	}
	
	// cEsA
	if(DmxValues[33] < SENSOR_ON_MAX && DmxValues[33] > SENSOR_ON_MIN) {
		WriteText("cEsA: proximity");
		LayerSetBlind(8+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(8+BASE_LAYERS,1); // hidden
	}
	// cEsB
	if(DmxValues[34] < SENSOR_ON_MAX && DmxValues[34] > SENSOR_ON_MIN) {
		WriteText("cEsB: proximity");
		LayerSetBlind(9+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(9+BASE_LAYERS,1); // hidden
	}
	
	// cFsA
	if(DmxValues[40] < SENSOR_ON_MAX && DmxValues[40] > SENSOR_ON_MIN) {
		WriteText("cEsA: proximity");
		LayerSetBlind(10+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(10+BASE_LAYERS,1); // hidden
	}
	// cFsB
	if(DmxValues[41] < SENSOR_ON_MAX && DmxValues[41] > SENSOR_ON_MIN) {
		WriteText("cFsB: proximity");
		LayerSetBlind(11+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(11+BASE_LAYERS,1); // hidden
	}
	
	// cGsA
	if(DmxValues[48] < SENSOR_ON_MAX && DmxValues[48] > SENSOR_ON_MIN) {
		WriteText("cGsA: proximity");
		LayerSetBlind(12+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(12+BASE_LAYERS,1); // hidden
	}
	// cGsB
	if(DmxValues[49] < SENSOR_ON_MAX && DmxValues[49] > SENSOR_ON_MIN) {
		WriteText("cGsB: proximity");
		LayerSetBlind(13+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(13+BASE_LAYERS,1); // hidden
	}
	
	// cHsA
	if(DmxValues[56] < SENSOR_ON_MAX && DmxValues[56] > SENSOR_ON_MIN) {
		WriteText("cHsA: proximity");
		LayerSetBlind(14+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(14+BASE_LAYERS,1); // hidden
	}
	// cHsB
	if(DmxValues[57] < SENSOR_ON_MAX && DmxValues[57] > SENSOR_ON_MIN) {
		WriteText("cHsB: proximity");
		LayerSetBlind(15+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(15+BASE_LAYERS,1); // hidden
	}
	
	// cIsA
	if(DmxValues[64] < SENSOR_ON_MAX && DmxValues[64] > SENSOR_ON_MIN) {
		WriteText("cIsA: proximity");
		LayerSetBlind(16+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(16+BASE_LAYERS,1); // hidden
	}
	// cIsB
	if(DmxValues[65] < SENSOR_ON_MAX && DmxValues[65] > SENSOR_ON_MIN) {
		WriteText("cIsB: proximity");
		LayerSetBlind(17+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(17+BASE_LAYERS,1); // hidden
	}
	
	// cJsA
	if(DmxValues[72] < SENSOR_ON_MAX && DmxValues[72] > SENSOR_ON_MIN) {
		WriteText("cJsA: proximity");
		LayerSetBlind(18+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(18+BASE_LAYERS,1); // hidden
	}
	// cJsB
	if(DmxValues[73] < SENSOR_ON_MAX && DmxValues[73] > SENSOR_ON_MIN) {
		WriteText("cJsB: proximity");
		LayerSetBlind(19+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(19+BASE_LAYERS,1); // hidden
	}
	
	// cKsA
	if(DmxValues[80] < SENSOR_ON_MAX && DmxValues[80] > SENSOR_ON_MIN) {
		WriteText("cKsA: proximity");
		LayerSetBlind(20+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(20+BASE_LAYERS,1); // hidden
	}
	// cKsB
	if(DmxValues[81] < SENSOR_ON_MAX && DmxValues[81] > SENSOR_ON_MIN) {
		WriteText("cKsB: proximity");
		LayerSetBlind(21+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(21+BASE_LAYERS,1); // hidden
	}
	
	// cLsA
	if(DmxValues[88] < SENSOR_ON_MAX && DmxValues[88] > SENSOR_ON_MIN) {
		WriteText("cLsA: proximity");
		LayerSetBlind(22+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(22+BASE_LAYERS,1); // hidden
	}
	// cLsB
	if(DmxValues[89] < SENSOR_ON_MAX && DmxValues[89] > SENSOR_ON_MIN) {
		WriteText("cLsB: proximity");
		LayerSetBlind(23+BASE_LAYERS,0); // visible
	}
	else {
		LayerSetBlind(23+BASE_LAYERS,1); // hidden
	}
	
	

}

void PostRenderEffect()
{

}

void MatrixSizeChanged()
{
	InitEffect();
}
