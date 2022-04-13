/*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

'use strict';

const { WorkloadModuleBase } = require('@hyperledger/caliper-core');

const rand = require('./random');

var deck = require('deck');
const unirand = require('unirand');

let x = 5;
let y = 40;
let xindex = 0;
let yindex = 0;
let functionindex = 0;
let otherfunctionindex = 0;
let argindex = 0;
let txnum = 10000;
let workernum = 10;
let txperworker = txnum/workernum;
let allfuncs = ["pushASN", "ship", "queryASN", "unload", "updateAuditInfo", "queryProducts"];
let criticalfuncs = [0, 1, 2, 3];
let otherfuncs = [4, 5]
let funcindexchangecount = txperworker/(criticalfuncs.length * 2)
let functionname = 0;
let locations = ["A", "B", "C", "D"];
let auditkey = 0;
let workerstartindex = 0; //Current worker pointer index
let workertxcount = 0; //Single function counter
let workerfirstcount = 0; //Single function initial count
/**
 * Workload module for the benchmark round.
 */
class CreateWorkload extends WorkloadModuleBase {

    /**
     * Initializes the workload module instance.
     */
    constructor() {
        super();
        this.txIndex = 0;
    }

    /**
     * Initialize the workload module with the given parameters.
     * @param {number} workerIndex The 0-based index of the worker instantiating the workload module.
     * @param {number} totalWorkers The total number of workers participating in the round.
     * @param {number} roundIndex The 0-based index of the currently executing round.
     * @param {Object} roundArguments The user-provided arguments for the round from the benchmark configuration file.
     * @param {BlockchainInterface} sutAdapter The adapter of the underlying SUT.
     * @param {Object} sutContext The custom context object provided by the SUT adapter.
     * @async
     */
    async initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext) {
        await super.initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext);

    }

    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
    async submitTransaction() {


	    if (this.txIndex == 0) {
		    workerstartindex = this.workerIndex * txperworker;
		    workertxcount = workerstartindex;
		    workerfirstcount = workerstartindex;
	    } else {
		    if ((workerstartindex % funcindexchangecount) == 0) {
			    workertxcount = workerfirstcount;
			    functionindex++
			    if (functionindex > (criticalfuncs.length -1)) {
				    workerfirstcount = workerstartindex;
				    workertxcount = workerfirstcount;
				    functionindex = 0;
			    }
	    
		    }
		   
		    argindex = functionindex;
		    if (xindex == x) {
			    xindex = 0
			    x = Math.floor(Math.random()*5)
			    argindex = otherfuncs[0]

		    } 
		   
		    if (yindex == y) {

			    yindex = 0
			    argindex = otherfuncs[1]
		    }
		    /*if (xindex == x) {

			    otherfunctionindex = otherfuncs[Math.floor(Math.random()*otherfuncs.length)];
			    argindex = otherfunctionindex;
			    x = 2 * x + 1;
			    if (xindex > 300) {

				    xindex = 0;
				    x = 5;
			    }
            
		    }*/
	    }



	    let today = new Date();
	    let tomorrow = new Date();
    	    tomorrow.setDate(today.getDate() + (unirand.random() * 10));
            let dateString = tomorrow.toString();

	    //let startkey = Math.floor(Math.random() * txnum)
	    //let endkey = Math.floor(Math.random() * (txnum - startkey + 1) + startkey)
	    let startkey = workertxcount
	    let endkey = workertxcount + 3

	    auditkey = Math.floor(Math.random() * 1000)

	    //let invkIdent = rand.getClient()
            //let targetOrg = rand.getEndorsers()

	    let funcargs = [
                {contractId : 'simplesupplychain', contractFunction: 'PushASN', contractArguments: [workertxcount.toString(), dateString, locations[Math.floor(Math.random()*locations.length)]], readOnly: false, timeout: 120},
                {contractId : 'simplesupplychain', contractFunction: 'Ship', contractArguments: [workertxcount.toString()], readOnly: false, timeout: 120},
                {contractId : 'simplesupplychain', contractFunction: 'QueryASN', contractArguments: [workertxcount.toString()], readOnly: false, timeout: 120},
                {contractId : 'simplesupplychain', contractFunction: 'Unload', contractArguments: [workertxcount.toString()], readOnly: false, timeout: 120},
                {contractId : 'simplesupplychain', contractFunction: 'UpdateAuditInfo', contractArguments: [(workertxcount - 2).toString(), auditkey.toString()], readOnly: false, timeout: 120}, 
		{contractId : 'simplesupplychain', contractFunction: 'QueryProducts', contractArguments: [startkey.toString(), endkey.toString()], readOnly: false, timeout: 120}
        ];


	    let args = funcargs[argindex];

	workerstartindex++
	workertxcount++
	this.txIndex++;
	xindex++;
	yindex++;
        await this.sutAdapter.sendRequests(args);

    }
}

/**
 * Create a new instance of the workload module.
 * @return {WorkloadModuleInterface}
 */
function createWorkloadModule() {
    return new CreateWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
