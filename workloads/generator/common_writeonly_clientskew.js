'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');
const { TxStatus } = require('@hyperledger/caliper-core');

const rand = require('./random_writeonly');
//const rand = require('./random');
const getParameters = require('./getParameters');


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

    /*async skipTransaction(){

	    const txstatus = new TxStatus('1')
	    txstatus.status.status = 'success'
	    txstatus.status.verified = true
	    return Promise.resolve(txstatus)

    }*/
    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
    async submitTransaction() {


	let args;
	let readonlyargs;
	let invkIdent = rand.getClient()
        let targetOrg = rand.getEndorsers()
	let funcnum = rand.getcontractFunction()
	let contractFunction = 'Func' + funcnum
	let contractArguments = rand.getcontractArguments(funcnum)

	var quotedAndCommaSeparated = '[' + "\"" + contractArguments.join("\",\"") + "\"" + ']';

/*
	args = { contractId: 'generator',
                contractVersion: 'v1',
                contractFunction: contractFunction,
                contractArguments: [quotedAndCommaSeparated],
		targetOrganizations: targetOrg,
                invokerIdentity: invkIdent,
                timeout: '30' }

	    
	contractArguments = rand.getcontractArguments(1)
        quotedAndCommaSeparated = '[' + "\"" + contractArguments.join("\",\"") + "\"" + ']';
	readonlyargs = { contractId: 'generator',
                    contractVersion: 'v1',
                    contractFunction: 'Func1',
                    contractArguments: [quotedAndCommaSeparated],
                    readOnly: true}

	    console.log(readonlyargs)
	    await this.sutAdapter.sendRequests(readonlyargs);

*/
	
	    //let clientorg1 =  'client0.org1.example.com'
	    //let clientorg2 =  'client1.org2.example.com'

        
	    if (this.workerIndex < 7) {
		    //let clientorg1 =  'client' + this.workerIndex + '.org1' + '.example.com'
		    let clientorg1 =  'client0.org1.example.com'
		    args = { contractId: 'generator',
               	    contractVersion: 'v1',
                    contractFunction: contractFunction,
                    contractArguments: [quotedAndCommaSeparated],
                    targetOrganizations: targetOrg,
                    invokerIdentity: clientorg1,
                    timeout: '30' }
		    await this.sutAdapter.sendRequests(args);
	    } 
	    else {
		    //let clientorg2 =  'client' + this.workerIndex + '.org2' + '.example.com'
		    let clientorg2 =  'client1.org2.example.com'
		    args = { contractId: 'generator',
                    contractVersion: 'v1',
                    contractFunction: contractFunction,
                    contractArguments: [quotedAndCommaSeparated],
                    targetOrganizations: targetOrg,
                    invokerIdentity: clientorg2,
                    timeout: '30' }
		    await this.sutAdapter.sendRequests(args);
	    }

	   /* 
	   
	    

	    if (this.workerIndex < 14) {
                    //let clientorg1 =  'client' + this.workerIndex + '.org1' + '.example.com'
		    let clientorg1 =  'client0.org1.example.com'
		    if (this.txIndex < 500) { 
                    	args = { contractId: 'generator',
                    		contractVersion: 'v1',
                    		contractFunction: contractFunction,
                    		contractArguments: [quotedAndCommaSeparated],
                    		targetOrganizations: targetOrg,
                    		invokerIdentity: clientorg1,
                    		timeout: '30' }
                    	await this.sutAdapter.sendRequests(args);
		    }
		    else {
		    	contractArguments = rand.getcontractArguments(1)
		    	quotedAndCommaSeparated = '[' + "\"" + contractArguments.join("\",\"") + "\"" + ']';
        	    	readonlyargs = { contractId: 'generator',
                    		contractVersion: 'v1',
                    		contractFunction: 'Func1',
                    		contractArguments: [quotedAndCommaSeparated],
                    		targetOrganizations: targetOrg,
                    		invokerIdentity: clientorg1,
                    		timeout: '30',
                    		readOnly: true}

			await this.sutAdapter.sendRequests(readonlyargs);
		    }
            }
            else {
                    //let clientorg2 =  'client' + this.workerIndex + '.org2' + '.example.com'
                    let clientorg2 =  'client1.org2.example.com'
		    args = { contractId: 'generator',
                    contractVersion: 'v1',
                    contractFunction: contractFunction,
                    contractArguments: [quotedAndCommaSeparated],
                    targetOrganizations: targetOrg,
                    invokerIdentity: clientorg2,
                    timeout: '30' }
                    await this.sutAdapter.sendRequests(args);
            }

	    */
	
	    this.txIndex++


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

