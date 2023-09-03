// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.4;

contract Order {
    uint public price;
    address payable public owner;
    address payable public courier;
    address public customer;
    //
    //    enum Status { Created, Pending, Complete }
    // The state variable has a default value of the first member, `State.created`
    //    Status public status;

    bool paid = false;
    bool confirmed = false;
    bool pickedUp = false;


    modifier condition(bool condition_) {
        require(condition_);
        _;
    }

    modifier onlyCustomer(){
        require(msg.sender == customer, "Invalid customer account.");
        _;
    }

    modifier onlyCourier(){
        require(msg.sender == courier, "Only couriers allowed");
        _;
    }
    modifier onlyOwner(){
        require(msg.sender == owner, "Only owners allowed");
        _;
    }
    modifier notPaid(){
        require(paid == false, "Transfer already complete.");
        _;
    }

    modifier alreadyPaid(){
        require(paid == true, "Transfer not complete.");
        _;
    }

    modifier confirmedDelivery(){
        require(confirmed == true, "Delivery not complete.");
        _;
    }

    modifier hasMoney(){
        require(customer.balance >= price, "Insufficient funds. SOLIDITY");
        _;
    }

    modifier notPickedUp(){
        require(pickedUp == false, "Already picked up");
        _;
    }

    modifier alreadyPickedUp(){
        require(pickedUp == true, "Delivery not complete.");
        _;
    }

    modifier notConfirmed(){
        require(confirmed == false, "Already confirmed!");
        _;
    }
    // Ensure that `msg.value` is an even number.
    // Division will truncate if it is an odd number.
    // Check via multiplication that it wasn't an odd number.
    constructor (address cust, uint pric) {
        owner = payable(msg.sender);
        customer = cust;
        price = pric;
    }


    /// Confirm the purchase as buyer.
    /// Transaction has to include `2 * value` ether.
    /// The ether will be locked until confirmReceived
    /// is called.
    function pay()
    external
    onlyCustomer
    hasMoney
    notPaid
    payable
    {
        paid = true;
    }

    function connectCurier(address courAdr)
    external
    alreadyPaid
    onlyOwner
    notPickedUp
    {
        courier = payable(courAdr);
        pickedUp = true;
    }


    function confirm()
    external
    onlyCustomer
    alreadyPaid
    alreadyPickedUp
    {
        confirmed = true;

        uint val = address(this).balance;
        uint own = (val * 80) / 100;
        uint cour = (val * 20) / 100;
        owner.transfer(own);
        courier.transfer(cour);
    }

}