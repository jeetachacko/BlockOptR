package main

import (
	"encoding/json"
	"fmt"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"

)

type SmartContract struct {
        contractapi.Contract
}

func main() {

        // Create a new Smart Contract
        chaincode, err := contractapi.NewChaincode(new(SmartContract))
        if err != nil {
                fmt.Printf("Error creating new Smart Contract: %s", err)
        }
        if err := chaincode.Start(); err != nil {
                fmt.Printf("Error starting chaincode: %s", err.Error())
        }

}

func (s *SmartContract) Init(ctx contractapi.TransactionContextInterface) error {
	return nil
}


/*func (s *SmartContract) Invoke(ctx contractapi.TransactionContextInterface) error {

	// Retrieve the requested Smart Contract function and arguments
	function, args := ctx.GetStub().GetFunctionAndParameters()
	// Route to the appropriate handler function to interact with the ledger appropriately
	if function == "initLedger" {
		return s.initLedger(ctx, args)
	} else if function == "doNothing" {
                return s.doNothing(ctx)
        } else if function == "func0" {
		return s.func0(ctx, args)
	} else if function == "func1" {
		return s.func1(ctx, args)
	} else if function == "func2" {
		return s.func2(ctx, args)
	} else if function == "func3" {
		return s.func3(ctx, args)
	} else if function == "func4" {
		return s.func4(ctx, args)
	} else if function == "func5" {
		return s.func5(ctx, args)
	} else if function == "func6" {
		return s.func6(ctx, args)
	} else if function == "func7" {
		return s.func7(ctx, args)
	} else if function == "func8" {
		return s.func8(ctx, args)
	} else if function == "func9" {
		return s.func9(ctx, args)
	} else if function == "func10" {
		return s.func10(ctx, args)
	} else if function == "func11" {
		return s.func11(ctx, args)
	} else if function == "func12" {
		return s.func12(ctx, args)
	} else if function == "func13" {
		return s.func13(ctx, args)
	} else if function == "func14" {
		return s.func14(ctx, args)
	} else if function == "func15" {
		return s.func15(ctx, args)
	} else if function == "func16" {
		return s.func16(ctx, args)
	} else if function == "func17" {
		return s.func17(ctx, args)
	} else if function == "func18" {
		return s.func18(ctx, args)
	}
	return fmt.Errorf("Invalid Smart Contract function name.")
}
*/

func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface, arg0 string, arg1 string) error {
	jvalue, _ := json.Marshal(arg1)
	ctx.GetStub().PutState(arg0, jvalue)

	return nil
}

func (s *SmartContract) DoNothing(ctx contractapi.TransactionContextInterface)  error {
	return nil
}
/*
		for key := 1; key <= args[0]; key++ {
			value := args[1] * 235
			ctx.GetStub().PutState(key, value)
		}
	return fmt.Error("Invalid Smart Contract function name.")
	return nil
}
*/

func (s *SmartContract) Func0(ctx contractapi.TransactionContextInterface, args []string) error {

	jvalue, _ := json.Marshal(args[1])
	ctx.GetStub().PutState(args[0], jvalue)
	return nil
}
/*	value, _ := ctx.GetStub().GetState(args[0])
	return nil
}*/

func (s *SmartContract) Func1(ctx contractapi.TransactionContextInterface, args []string) error {

	//Read key
	value, _ := ctx.GetStub().GetState(args[0])
	//Read key
	value, _ = ctx.GetStub().GetState(args[1])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func2(ctx contractapi.TransactionContextInterface, args []string) error {

	//Read key
	value, _ := ctx.GetStub().GetState(args[0])
	//Read key
	value, _ = ctx.GetStub().GetState(args[1])
	//Read key
	value, _ = ctx.GetStub().GetState(args[2])
	//Read key
	value, _ = ctx.GetStub().GetState(args[3])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func3(ctx contractapi.TransactionContextInterface, args []string) error {

	//Read key
	value, _ := ctx.GetStub().GetState(args[0])
	//Read key
	value, _ = ctx.GetStub().GetState(args[1])
	//Read key
	value, _ = ctx.GetStub().GetState(args[2])
	//Read key
	value, _ = ctx.GetStub().GetState(args[3])
	//Read key
	value, _ = ctx.GetStub().GetState(args[4])
	//Read key
	value, _ = ctx.GetStub().GetState(args[5])
	//Read key
	value, _ = ctx.GetStub().GetState(args[6])
	//Read key
	value, _ = ctx.GetStub().GetState(args[7])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func4(ctx contractapi.TransactionContextInterface, args []string) error {

	//Insert new key
	jvalue, _ := json.Marshal(args[1])
	ctx.GetStub().PutState(args[0], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[3])
	ctx.GetStub().PutState(args[2], jvalue)

	return nil
}
func (s *SmartContract) Func5(ctx contractapi.TransactionContextInterface, args []string) error {

	//Insert new key
	jvalue, _ := json.Marshal(args[1])
	ctx.GetStub().PutState(args[0], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[3])
	ctx.GetStub().PutState(args[2], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[5])
	ctx.GetStub().PutState(args[4], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[7])
	ctx.GetStub().PutState(args[6], jvalue)

	return nil
}
func (s *SmartContract) Func6(ctx contractapi.TransactionContextInterface, args []string) error {

	//Insert new key
	jvalue, _ := json.Marshal(args[1])
	ctx.GetStub().PutState(args[0], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[3])
	ctx.GetStub().PutState(args[2], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[5])
	ctx.GetStub().PutState(args[4], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[7])
	ctx.GetStub().PutState(args[6], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[9])
	ctx.GetStub().PutState(args[8], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[11])
	ctx.GetStub().PutState(args[10], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[13])
	ctx.GetStub().PutState(args[12], jvalue)
	//Insert new key
	jvalue, _ = json.Marshal(args[15])
	ctx.GetStub().PutState(args[14], jvalue)

	return nil
}
func (s *SmartContract) Func7(ctx contractapi.TransactionContextInterface, args []string) error {

	//Update a key
	value, _ := ctx.GetStub().GetState(args[0])
	valuex := args[1]
	jvalue, _ := json.Marshal(valuex)

	ctx.GetStub().PutState(args[0], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[2])
	valuex = args[3]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[2], jvalue)
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func8(ctx contractapi.TransactionContextInterface, args []string) error {

	//Update a key
	value, _ := ctx.GetStub().GetState(args[0])
	valuex := args[1]
	jvalue, _ := json.Marshal(valuex)

	ctx.GetStub().PutState(args[0], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[2])
	valuex = args[3]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[2], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[4])
	valuex = args[5]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[4], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[6])
	valuex = args[7]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[6], jvalue)
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func9(ctx contractapi.TransactionContextInterface, args []string) error {

	//Update a key
	value, _ := ctx.GetStub().GetState(args[0])
	valuex := args[1]
	jvalue, _ := json.Marshal(valuex)

	ctx.GetStub().PutState(args[0], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[2])
	valuex = args[3]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[2], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[4])
	valuex = args[5]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[4], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[6])
	valuex = args[7]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[6], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[8])
	valuex = args[9]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[8], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[10])
	valuex = args[11]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[10], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[12])
	valuex = args[13]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[12], jvalue)
	//Update a key
	value, _ = ctx.GetStub().GetState(args[14])
	valuex = args[15]
	jvalue, _ = json.Marshal(valuex)

	ctx.GetStub().PutState(args[14], jvalue)
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func10(ctx contractapi.TransactionContextInterface, args []string) error {

	//Delete a key
	ctx.GetStub().DelState(args[0])
	//Delete a key
	ctx.GetStub().DelState(args[1])

	return nil
}
func (s *SmartContract) Func11(ctx contractapi.TransactionContextInterface, args []string) error {

	//Delete a key
	ctx.GetStub().DelState(args[0])
	//Delete a key
	ctx.GetStub().DelState(args[1])
	//Delete a key
	ctx.GetStub().DelState(args[2])
	//Delete a key
	ctx.GetStub().DelState(args[3])

	return nil
}
func (s *SmartContract) Func12(ctx contractapi.TransactionContextInterface, args []string) error {

	//Delete a key
	ctx.GetStub().DelState(args[0])
	//Delete a key
	ctx.GetStub().DelState(args[1])
	//Delete a key
	ctx.GetStub().DelState(args[2])
	//Delete a key
	ctx.GetStub().DelState(args[3])
	//Delete a key
	ctx.GetStub().DelState(args[4])
	//Delete a key
	ctx.GetStub().DelState(args[5])
	//Delete a key
	ctx.GetStub().DelState(args[6])
	//Delete a key
	ctx.GetStub().DelState(args[7])

	return nil
}
func (s *SmartContract) Func13(ctx contractapi.TransactionContextInterface, args []string) error {

	//Get range of keys
	value, _ := ctx.GetStub().GetStateByRange(args[0], args[1])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[2], args[3])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func14(ctx contractapi.TransactionContextInterface, args []string) error {

	//Get range of keys
	value, _ := ctx.GetStub().GetStateByRange(args[0], args[1])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[2], args[3])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[4], args[5])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[6], args[7])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func15(ctx contractapi.TransactionContextInterface, args []string) error {

	//Get range of keys
	value, _ := ctx.GetStub().GetStateByRange(args[0], args[1])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[2], args[3])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[4], args[5])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[6], args[7])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[8], args[9])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[10], args[11])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[12], args[13])
	//Get range of keys
	value, _ = ctx.GetStub().GetStateByRange(args[14], args[15])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func16(ctx contractapi.TransactionContextInterface, args []string) error {

	//Query using query string
	value, _ := ctx.GetStub().GetQueryResult(args[0])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[1])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func17(ctx contractapi.TransactionContextInterface, args []string) error {

	//Query using query string
	value, _ := ctx.GetStub().GetQueryResult(args[0])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[1])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[2])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[3])
	_ = value
	fmt.Println(value)

	return nil
}
func (s *SmartContract) Func18(ctx contractapi.TransactionContextInterface, args []string) error {

	//Query using query string
	value, _ := ctx.GetStub().GetQueryResult(args[0])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[1])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[2])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[3])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[4])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[5])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[6])
	//Query using query string
	value, _ = ctx.GetStub().GetQueryResult(args[7])
	_ = value
	fmt.Println(value)

	return nil
}
/*func main() {

	// Create a new Smart Contract
	chaincode, err := contractapi.NewChaincode(new(SmartContract))
	if err != nil {
		fmt.Printf("Error creating new Smart Contract: %s", err)
	}
	if err := chaincode.Start(); err != nil {
                fmt.Printf("Error starting chaincode: %s", err.Error())
        }

}*/
