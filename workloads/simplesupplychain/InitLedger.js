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

     async initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext) {
        await super.initializeWorkloadModule(workerIndex, totalWorkers, roundIndex, roundArguments, sutAdapter, sutContext);

    }


    /**
     * Assemble TXs for the round.
     * @return {Promise<TxStatus[]>}
     */
	//if(this.workerIndex == 0) {
		async submitTransaction() {
			this.txIndex++;
			let args = {
				contractId: 'simplesupplychain',
				contractFunction: 'InitLedger',
				contractArguments: [],
				readOnly: false,
				timeout: 120,
			};
			console.log("ARGS:")
            		console.log(args)
			await this.sutAdapter.sendRequests(args);
			}
	//}
	
}

/**
 * Create a new instance of the workload module.
 * @return {WorkloadModuleInterface}
 */
function createWorkloadModule() {
    return new CreateWorkload();
}

module.exports.createWorkloadModule = createWorkloadModule;
