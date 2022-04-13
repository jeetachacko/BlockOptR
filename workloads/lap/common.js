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
const fs = require('fs');
//const pd = require("node-pandas")
const { WorkloadModuleBase } = require('@hyperledger/caliper-core');


/**
 * Workload module for the benchmark round.
 */
class Common extends WorkloadModuleBase {
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

        // await helper.createCar(this.sutAdapter, this.workerIndex, this.roundArguments);
    }

    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
    async submitTransaction() {
        this.txIndex++;

	let df = fs.readFileSync(__dirname + "/" + this.workerIndex + "_transactions.csv").toString().split("\n");

	//df = pd.readCsv(__dirname + "/" + this.workerIndex + "_transactions.csv")
	let firsttempargs = df[this.txIndex]
	console.log(firsttempargs)
	let tempargs = firsttempargs.split(',')
	let numargs = tempargs.length
	console.log(numargs)

	let args;
	if(numargs >= 5){

		args = {
			contractId: 'lapnew',
            		contractVersion: 'v1',
            		contractFunction: tempargs[0].trim(),
            		contractArguments: [tempargs[1].trim(), tempargs[2].trim(), tempargs[3].trim(), tempargs[4].trim(), tempargs[5].trim()]
        		};
	}
	else if(numargs >= 3){
		args = {
                        contractId: 'lapnew',
                        contractVersion: 'v1',
                        contractFunction: tempargs[0].trim(),
                        contractArguments: [tempargs[1].trim(), tempargs[2].trim(), tempargs[3].trim()]
                        };

	}
	else {
		args = {
                        contractId: 'lapnew',
                        contractVersion: 'v1',
                        contractFunction: tempargs[0].trim(),
                        contractArguments: [tempargs[1].trim(), tempargs[2].trim()]
                        };
	}

	console.log(args)
        await this.sutAdapter.sendRequests(args);
    }
}

/**
 * Create a new instance of the workload module.
 * @return {WorkloadModuleInterface}
 */
function createWorkloadModule() {
    return new Common();
}

module.exports.createWorkloadModule = createWorkloadModule;
