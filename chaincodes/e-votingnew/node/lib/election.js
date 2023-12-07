'use strict';

class Election {
    constructor(allParty, allVoter, electionClosed) {
        this.docType = 'election';
        this.allParty = (allParty === undefined) ? {} : allParty;
	this.allVoter = (allVoter === undefined) ? {} : allVoter;
        this.electionClosed = (electionClosed === undefined) ? false : electionClosed;
    }

    static fromJSON(obj) {
        if (obj.allParty !== undefined && obj.allVoter !== undefined) {
            return new Election(obj.allParty, obj.allVoter, obj.electionClosed);
        }
    }

    /**
     * Return a world-state ids for the parties taking part of the election.
     */
    get allPartyId() {
        return (this.allParty === undefined) ? [] :  Object.keys(this.allParty);
    }

    get allVoterId() {
        return (this.allVoter === undefined) ? [] :  Object.values(this.allVoter);
    }


    /**
     * Sets a supplied count to a partys result if the party was part of the election.
     * @param {String} partyId
     * @param {Number} count
     */
    addCountToParty(partyId, count) {
        if (this.allParty !== undefined) {
            if (this.allParty.hasOwnProperty(partyId)) {
                this.allParty[partyId] = count;
            }
        }
    }

    /**
     * Returns the results of the election with the winning party leading the list.
     * @param {Object{String,Number}} allPartyResult
     */
    static electionResultsDescending(allPartyResult) {
	console.log('electionResultsDescending')
        let electionResults = [];
        for (const party in allPartyResult) {
		 console.log('infor');
            electionResults.push([party, allPartyResult[party]]);
        }
	     console.log('electionResults');
	    console.log(electionResults);
        electionResults.sort(function(a, b) {
		console.log('sort');
            return b[1] - a[1];
        });
	    console.log('aftersort');
        return electionResults;
    }
}

module.exports = Election;
