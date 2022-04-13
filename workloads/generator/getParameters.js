'use strict';
class getParameters {

    static keyPickerType() {
	//keyPickerType values: 0==zipfian, 1==hotkey 
        let keyPickerType = 0;
	return keyPickerType;
   }
   static zipfianSkew() {
        //zipfianSkew values: 0==uniform, Negative==HigherValues, Positive==LowerValues
        let zipfianSkew = 0;
        return zipfianSkew;
   }
   static hotKeyProb() {
        let hotKeyProb = 90;
        return hotKeyProb;
   }
   static hotKeyNum() {
        let hotKeyNum = 50;
        return hotKeyNum;
   }

    static chaincodeType() {
	//chaincodeType values: 0==Uniform, 1==ReadHeavy, 2==WriteHeavy
        let chaincodeType = 0;
        return chaincodeType;
   }
   static readWriteProb() {
        let readWriteProb = 50;
        return readWriteProb;
   }
   static clientDist() {
	//clientDist values: 0==uniform, Negative==HigherValues, Positive==LowerValues
	let clientDist = 0;
	return clientDist;
   }
   static endorserDist() {
        //endorserDist values: 0==uniform, Negative==HigherValues, Positive==LowerValues
        let endorserDist = 0;
        return endorserDist;
   }
   static clientorgDist() {
	   //clientorgDist values: 0==uniform, Negative==HigherValues, Positive==LowerValues
	let clientorgDist = 0;
	return clientorgDist;
   }

	//TODO: Get NClients, NEndorsers, NOrgs from config file
   static getNClients() {
	let NClients = 5;
	return NClients;
   }
   static getNEndorsers() {
        let NEndorsers = 2;
	return NEndorsers;
   }
   static gettotalNEndorsers() {
        let tNEndorsers = 2;
        return tNEndorsers;
   }

   static getNOrgs() {
        let NOrgs = 2;
	return NOrgs;
   }

   static genWorkload() {
	//0==uniform, 1==RH, 2==UH, 3==IH, 4==RRH, 5==readonly, 6==writeonly
        let workload = 0;
	return workload;
   }

   static genKeySkew() {
	// 0==uniform, Negative==HigherValues, Positive==LowerValues
        let keyskew = 1;
	   return keyskew;
   }
   static getendPol() {
        // 0==Majority, 1:And(o1,o2), 2:And(allO), 3:And(o1,or(o2,03,04), 4:And(or(o1,o2),or(o3,o4))
        let endpol = 0;
        return endpol;
   }


}

module.exports = getParameters;

