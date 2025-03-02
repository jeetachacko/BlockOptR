/* eslint-disable no-undef */
'use strict';

const rand = require('./random');
const seeds = require('./seeds');
const getParameters = require('./getParameters');

class addEhr {

    static get() {
	    let args;
	    let standardDerivation = getParameters.keyPickerType();
	    let randomAccessKey = rand.randomIndex(seeds.allActor.length, standardDerivation);

	    while (seeds.allActor[randomAccessKey] === undefined) {
	        randomAccessKey = rand.randomIndex(seeds.allActor.length, standardDerivation);
	    }

	    let actor = seeds.allActor[randomAccessKey];

	    let randomAccessKey2 = rand.randomIndex(seeds.allSSN.length, standardDerivation);

	    while (seeds.allSSN[randomAccessKey2] === undefined) {
	        randomAccessKey2 = rand.randomIndex(seeds.allSSN.length, standardDerivation);
	    }

	    let ssn = seeds.allSSN[randomAccessKey2];

	    let randomAccessKey3 = rand.randomIndex(seeds.allEhrFreeId.length, standardDerivation);

	    while (seeds.allEhrFreeId[randomAccessKey3] === undefined) {
	        randomAccessKey3 = rand.randomIndex(seeds.allEhrFreeId.length, standardDerivation);
	    }

	    let ehr = seeds.allEhrFree[seeds.allEhrFreeId[randomAccessKey3]];
	    let ehrId = seeds.allEhrFreeId[randomAccessKey3];

	    //console.info(ehr);

	    let invkIdent = rand.getClient()
            let targetOrg = rand.getEndorsers()
	    args = {
                contractId: 'electronic-health-record',
                contractVersion: 'v1',
                contractFunction: 'addEHR',
                contractArguments: [ssn, `${actor}`, ehr, ehrId],
                // targetOrganizations: targetOrg,
                // invokerIdentity: invkIdent,
		timeout: 30
            };

	    return args;

	}
}

module.exports = addEhr;
