// SPDX-License-Identifier: MIT
pragma solidity ^0.8.25;

contract MedicalBilling {
    
    struct Bill {
        string patientId;
        uint256 date;
        string visitType;
        string diagnosis;
        uint256 amount;
        address paymentToken;
        bool paid;
    }

    mapping(string => Bill) private bills;
    address public owner;

    event BillSubmitted(string patientId, uint256 date, string visitType, string diagnosis, uint256 amount, address paymentToken);
    event BillPaid(string patientId, uint256 amount, address paymentToken);

    constructor() {
        owner = msg.sender;
    }

    // Submit a new bill for a patient
    function submitBill(
        string memory _patientId,
        uint256 _date,
        string memory _visitType,
        string memory _diagnosis,
        uint256 _amount,
        address _paymentToken
    ) public {
        require(bills[_patientId].date == 0, "Bill already exists for this patient ID");

        bills[_patientId] = Bill({
            patientId: _patientId,
            date: _date,
            visitType: _visitType,
            diagnosis: _diagnosis,
            amount: _amount,
            paymentToken: _paymentToken,
            paid: false
        });

        emit BillSubmitted(_patientId, _date, _visitType, _diagnosis, _amount, _paymentToken);
    }

    // Get bill details by patient ID
    function getBill(string memory _patientId) public view returns (Bill memory) {
        require(bills[_patientId].date != 0, "Bill not found");
        return bills[_patientId];
    }

    // Pay a bill
    function payBill(string memory _patientId) public payable {
        Bill storage bill = bills[_patientId];
        require(bill.date != 0, "Bill not found");
        require(!bill.paid, "Bill already paid");

        require(msg.value == bill.amount, "Incorrect payment amount");
        bill.paid = true;

        // Transfer the payment to the contract owner
        payable(owner).transfer(msg.value);

        emit BillPaid(_patientId, bill.amount, bill.paymentToken);
    }

    // Withdraw funds by the owner
    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }
}
