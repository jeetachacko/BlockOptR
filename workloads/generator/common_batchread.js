'use strict';


let rand = require('./random');
const randr = require('./random_readonly');
const randw = require('./random_writeonly');
const getParameters = require('./getParameters');
const { WorkloadModuleBase } = require('@hyperledger/caliper-core');


var fs = require('fs');
const zeroPad = (num, places) => String(num).padStart(places, '0')


let index = 0
let fileIndex = 0
//let txIndex = 0
let filearray = [];
let err = 0

/**
 * Workload module for the benchmark round.
 */
class CreateCarWorkload extends WorkloadModuleBase {
    /**
     * Initializes the workload module instance.
     */
    constructor() {
        super();
        this.txIndex = 0;
    }
    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
    async submitTransaction() {


	if (this.txIndex < 500){
		rand = randr
	}
	else {
		rand = randw
	}
	this.txIndex++;	
	let args;
	let invkIdent = rand.getClient()
        //let targetOrg = rand.getEndorsers()
	let funcnum = rand.getcontractFunction()
	let contractFunction = 'Func' + funcnum
	let contractArguments = rand.getcontractArguments(funcnum)

	var quotedAndCommaSeparated = '[' + "\"" + contractArguments.join("\",\"") + "\"" + ']';

	//console.log(targetOrg)

	args = { contractId: 'generator',
                contractVersion: 'v1',
                contractFunction: contractFunction,
                contractArguments: [quotedAndCommaSeparated],
		targetOrganizations: ['Org1MSP','Org2MSP'],
                invokerIdentity: invkIdent,
                timeout: '30' }
        

	    await this.sutAdapter.sendRequests(args);

    }
}

/**
 * Create a new instance of the workload module.
 * @return {WorkloadModuleInterface}
 */
function createWorkloadModule() {
	filearray = [];
    return new CreateCarWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;

