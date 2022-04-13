/*
SPDX-License-Identifier: Apache-2.0
*/

package main

import (
	"encoding/json"
	"fmt"
//	"strconv"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// SmartContract provides functions for managing a loan application
type SmartContract struct {
	contractapi.Contract
}

// Application describes basic details of what makes up a loan application
type Application struct {
	ID   string `json:"id"`
	Status  string `json:"status"`
	Amount string `json:"amount"`
	Goal  string `json:"goal"`
	Empid   string `json:"empid"`
}

// QueryResult structure used for handling result of query
type QueryResult struct {
	Key    string `json:"Key"`
	Record *Application
}


//Insert ID, status Created, amount, goal
func (s *SmartContract) SubmitApplication(ctx contractapi.TransactionContextInterface, empid string, id string, status string, amount string, goal string) error {
        app := Application{
                ID:   id,
                Status:  status,
                Amount: amount,
                Goal:  goal,
		Empid: empid,
        }

        appAsBytes, _ := json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Concept(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Accepted(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Complete(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Validating(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Incomplete(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Pending(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Denied(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

func (s *SmartContract) A_Cancelled(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}


//ReadWrite ID,status
/*func (s *SmartContract) SendDocumentation(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

        app.Status = status

        appAsBytes, _ = json.Marshal(app)

        return ctx.GetStub().PutState(id, appAsBytes)
}

*/
//Read ID
/*func (s *SmartContract) ReadApplicationStatus(ctx contractapi.TransactionContextInterface, empid string, id string) (*Application, error) {

        appAsBytes, err := ctx.GetStub().GetState(id)

        if err != nil {
                return nil, fmt.Errorf("Failed to read from world state. %s", err.Error())
        }

        if appAsBytes == nil {
                return nil, fmt.Errorf("%s does not exist", id)
        }

        app := new(Application)
        _ = json.Unmarshal(appAsBytes, app)

	return app, nil

}
*/
//ReadWrite ID, status
//func (s *SmartContract) SetApplicationStatus(ctx contractapi.TransactionContextInterface, empid string, id string, status string) error {
//
//        appAsBytes, err := ctx.GetStub().GetState(id)
//
//        if err != nil {
//                return fmt.Errorf("Failed to read from world state. %s", err.Error())
//        }
//
//        if appAsBytes == nil {
//                return fmt.Errorf("%s does not exist", id)
//        }
//
//        app := new(Application)
//        _ = json.Unmarshal(appAsBytes, app)
//
//        app.Status = status

//        appAsBytes, _ = json.Marshal(app)

//        return ctx.GetStub().PutState(id, appAsBytes)
//}



func main() {

	chaincode, err := contractapi.NewChaincode(new(SmartContract))

	if err != nil {
		fmt.Printf("Error create lap chaincode: %s", err.Error())
		return
	}

	if err := chaincode.Start(); err != nil {
		fmt.Printf("Error starting lap chaincode: %s", err.Error())
	}
}
