'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

const getParameters = require('./getParameters');
const queryParties = require('./queryParties');
const seeResults = require('./seeResults');
const vote = require('./vote');
const fs = require('fs');
const read = require('read-yaml');
const KnuthShuffle = require('./knuthShuffle');
const random = require('./random');
var deck = require('deck');
var Picker = require('random-picker').Picker;

let keyIndex = 0;
let nclients = 10
let ntransactions = 1000
let tranperclient = ntransactions/nclients


const ALLTESTCASE = [
    vote
];
let readHeavy = [0];
let writeHeavy = [0];


// PROVIDE NUMBER OF TESTCASES
let testCasePermuation = [
    0
];

let permutationsToCompute = 1;

function isDefined(t) {
  if (t === undefined) {
     return false;
  }
  return true;
}

class CreateCarWorkload extends WorkloadModuleBase {
    constructor() {
        super();
        this.txIndex = 0;
    }
    async submitTransaction() {

	keyIndex = this.txIndex + (this.workerIndex * tranperclient);


        this.txIndex++;


    let args;
    let chaincodeType = getParameters.chaincodeType();
    var picker = new Picker(); 
    let prob = getParameters.readWriteProb();
    picker.option(0, prob);
    var nprob = 100 - prob;
    picker.option(1, nprob);

    if (chaincodeType == 0) {
	let uniformPick = deck.pick(testCasePermuation);
	args = ALLTESTCASE[uniformPick].get(keyIndex);
    }
    else if (chaincodeType == 1) {
	let weightedPick = 0;
	if (picker.pick() == 0) {	
		weightedPick = deck.pick(readHeavy);
	}
	else {
		weightedPick = deck.pick(writeHeavy);
	}
	args = ALLTESTCASE[weightedPick].get(keyIndex);
    }
    else if (chaincodeType == 2) {
	let weightedPick = 0;
        if (picker.pick() == 0) {
                weightedPick = deck.pick(writeHeavy);
        }
        else {
                weightedPick = deck.pick(readHeavy);
        }
        args = ALLTESTCASE[weightedPick].get(keyIndex);
    }

        await this.sutAdapter.sendRequests(args);
    }
}
function createWorkloadModule() {
    return new CreateCarWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
