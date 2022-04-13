'use strict';

const unirand = require('unirand');
const getParameters = require('./getParameters');
var zipfian  = require("zipfian-integer")
var deck = require('deck');
var Picker = require('random-picker').Picker;
let hotKeyProb = getParameters.hotKeyProb();
var picker = new Picker();
picker.option(0, hotKeyProb);
picker.option(1, 100 - hotKeyProb);

class Random {

    static randomIndex(sizeKeyspace, keyPickerType) {
	if (keyPickerType == 0) {
		let skew = getParameters.zipfianSkew();
		const index = zipfian(1, sizeKeyspace-1, skew);
		return index();
	}
	else if (keyPickerType == 1) {
		let hotKeyNumPer = getParameters.hotKeyNum();
		let hotKeyNum = Math.round((hotKeyNumPer/100)*sizeKeyspace) 
		if (picker.pick() == 0) {
			const index = zipfian(1, hotKeyNum, 0);
			return index();
		}
		else if (picker.pick() == 1) {
                        const index = zipfian(hotKeyNum+1, sizeKeyspace-1, 0);
                        return index();
                }

        }

    }
    static getClient() {
	let clientDist = getParameters.clientDist();
	let clientorgDist = getParameters.clientorgDist(); 
	let nclients = getParameters.getNClients();
	let norgs = getParameters.getNOrgs();
	const clientindex = zipfian(0, nclients-1, clientDist);
	const orgindex = zipfian(1, norgs-1, clientorgDist);
	let client =  'client' + clientindex() + '.org' + orgindex() + '.example.com' 
	return client;
    }
    static getEndorsers() {
	let endpol = getParameters.getendPol();
	let endorserDist = getParameters.endorserDist();
	let norgs = getParameters.gettotalNEndorsers();
	let nendorsers = getParameters.getNEndorsers();
	let endorsers = new Array();

	if (norgs == nendorsers) {
		for (let i = 0; i < nendorsers; i++) {
			let index = i+1
			endorsers = endorsers.concat('Org'+index+'MSP')
		}
		return endorsers;
	}
	 if (endpol == 3){
                endorsers = endorsers.concat('Org1MSP')
                let endindex  = zipfian(2, norgs, endorserDist);
                let index = endindex()
                endorsers = endorsers.concat('Org'+index+'MSP')
                return endorsers;
        }


        if (endpol == 4){
		let endindex  = zipfian(1, (norgs/2), endorserDist);
		let index = endindex()
                endorsers = endorsers.concat('Org'+index+'MSP')
		endindex  = zipfian(((norgs/2)+1), norgs, endorserDist);
                index = endindex()
                endorsers = endorsers.concat('Org'+index+'MSP')

                return endorsers;
        }

	let endindex  = zipfian(1, norgs, endorserDist);
	let tempendorsers = new Array();
	for (let i = 0; i < nendorsers; i++) {
		let index = endindex()
		while((tempendorsers.includes(index))){
			index = endindex()
		}
		tempendorsers[i] = index; 
        	endorsers = endorsers.concat('Org'+index+'MSP')

	}
	
	return endorsers;
    }
    static getcontractFunction(){

	    let genWorkload = getParameters.genWorkload();
	    var x
	    console.log(genWorkload)
	    //genWorkload == 0==uniform, 1==RH, 2==UH, 3==IH, 4==RRH
	    //Function index == 1:Read, 4:Insert, 7:update, 10:delete, 13:range
	    if (genWorkload == 0) {
		x = deck.pick({1 : 10, 4 : 10, 7 : 10, 10 : 0, 13 : 0,});
		    return x
	    }
	    else if (genWorkload == 1) {
		x = deck.pick({1 : 10, 4 : 3, 7 : 3, 10 : 0, 13 : 0,});
                    return x

	    }
	    else if (genWorkload == 2) {
                x = deck.pick({1 : 3, 4 : 10, 7 : 3, 10 : 0, 13 : 0,});
                    return x

	    }
	    else if (genWorkload == 3) {
                x = deck.pick({1 : 3, 4 : 10, 7 : 3, 10 : 0, 13 : 0,});
                    return x

	    }
	    else if (genWorkload == 4) {

                x = deck.pick({1 : 3, 4 : 3, 7 : 3, 10 : 0, 13 : 10,});
                    return x

	    }


    }
    static getcontractArguments(functype){

	    console.log(functype)
	    let numberOfArgs;
	    const constantMultiplier = 100
	    let sizeKeySpace = 10000
	    let keyDisttribution = getParameters.genKeySkew()
	    let argments = new Array()
	    if (functype == 1) {
		numberOfArgs = 2
		for (let i = 0; i < numberOfArgs; i++) {
	                const keyfunc = zipfian(1, sizeKeySpace, keyDisttribution)
                        let key = keyfunc()
                        	argments[i] = key.toString()
                }

		//var quotedAndCommaSeparated = '[' + "\"" + argments.join("\",\"") + "\"" + ']';
	        return argments;
	    }
	    else if (functype == 4) {
		numberOfArgs = 4
  	        let argments = new Array()
                for (let i = 0; i < numberOfArgs; i=i+2) {
                	const keyfunc = zipfian(sizeKeySpace, sizeKeySpace*2, keyDisttribution)
                        let key = keyfunc()
                        argments[i] = key.toString()
                        argments[i+1] = (key * constantMultiplier).toString()
                }
		return argments;

	    }
	    else if (functype == 7) {
		numberOfArgs = 4
		let argments = new Array()
                for (let i = 0; i < numberOfArgs; i=i+2) {
                	const keyfunc = zipfian(1, sizeKeySpace, keyDisttribution)
                        let key = keyfunc()
                        argments[i] = key.toString()
                        argments[i+1] = constantMultiplier.toString()
                }
		    return argments;

	    }
	    else if (functype == 10) {

		numberOfArgs = 2
		let argments = new Array()
                for (let i = 0; i < numberOfArgs; i++) {
                	const keyfunc = zipfian(1, (sizeKeySpace - 2), keyDisttribution)
                        let key = keyfunc()
                        argments[i] = key.toString()
                }
		    return argments;

	    }
	    else if (functype == 13) {

		const rangeLength = [2, 4, 8]
		numberOfArgs = 4
		let argments = new Array()
                for (let i = 0; i < numberOfArgs; i=i+2) {
                	const keyfunc = zipfian(1, sizeKeySpace, keyDisttribution)
                        let key = keyfunc()
                        argments[i] = key.toString()
                        let range = deck.pick(rangeLength)
                        if ((key + range) >= sizeKeySpace) {
 	                       argments[i+1] = (sizeKeySpace - 1).toString()
                        }
                        else {
	                        argments[i+1] = (key + range).toString()
                        }
               }
		    return argments;

	    }


    }


    static randomZeroToTen() {
        // uniformly distributed on domain [0,1)
        return unirand.random() * 10;
    }

    static uniformNatural(upper) {
        return Math.ceil(unirand.random() * upper);
    }

    static standardNormalNatural(upper, deviation) {
        let mu = upper / 2;
        let random = unirand.normal(mu, deviation).randomSync();
        return Math.round(random);
    }
}

module.exports = Random;
