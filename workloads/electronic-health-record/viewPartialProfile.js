/* eslint-disable no-undef */
'use strict';

const rand = require('./random');
const seeds = require('./seeds');
const getParameters = require('./getParameters');

/*module.exports.info = 'View partial patient profile';

let bc, contx, standardDerivation;
module.exports.init = function (blockchain, context, args) {
    bc = blockchain;
    contx = context;
    standardDerivation = rand.randomZeroToTen();
    return Promise.resolve();
};

module.exports.run = function () {*/

class viewPartialProfile {

    static get() {
    let standardDerivation = getParameters.keyPickerType();
    let args;
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

	    let invkIdent = rand.getClient()
            let targetOrg = rand.getEndorsers()
    //if (bc.bcType === 'fabric-ccp') {
            args = {
                contractId: 'electronic-health-record',
                contractVersion: 'v1',
                contractFunction: 'viewPartialProfile',
                contractArguments: [ssn, `${actor}`],
                 // targetOrganizations: targetOrg,
                // invokerIdentity: invkIdent,
                timeout: 30
            };

    //}
        return args;

        }
}

module.exports = viewPartialProfile;



/*
    return bc.invokeSmartContract(
        contx,
        'electronic-health-record',
        'v1',
        args,
        120
    );
};

module.exports.end = function () {
    return Promise.resolve();
};
*/
