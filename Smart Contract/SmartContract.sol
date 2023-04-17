<<<<<<< HEAD
pragma solidity ^0.8.18;

contract semcoin_ico{
//we will first define three variables, 1) total number of coins, 2) coin to usd conversion rate, 3) total number of coins bought till now 

uint public max_semcoin = 1000000;        //Max coins that can be circulation
uint public usd_to_semcoin = 1000;         //1 usd equals 1000 semcoin right now
uint public total_semcoin_bought = 0;      //We will initialise to 0 because we haven't sold any


//We will create a mapping to the investor’s address with our coin’s equity and usd. Mapping is like a function, but the data is stored in an array.
mapping (address=> uint) equity_semcoin;              //address is a type in solidity
mapping (address=> uint) equity_usd;                  //mapping will take address as input and return unsigned integer as output with name as equity_usd


//With the help of a modifier we will check if an investor can buy our coin with a certain amount of usd
modifier can_buy_coins(uint usd_invested){
    //we will use a function called require which will check if the condition is true or not
    require (usd_invested * usd_to_semcoin + total_semcoin_bought <= max_semcoin);
    _;  //this tells compiler that the function that is linked with the modifier should only run if the condition is verified.
}

//We will create two functions to check the equity of investor in coin and in usd
function equity_held_semcoin(address investor) external view returns(uint) {
    return equity_semcoin[investor];
}

function equity_held_usd(address investor) external view returns(uint) {
    return equity_usd[investor];
}


//We will now make a function to buy coins in our ether wallet. 
//This function will take two arguments 1st the address of investor and 2nd how much dollar investor want to spend.
//First we will check if they can buy or not
function buy_semcoin(address investor, uint usd_invested) external can_buy_coins(usd_invested){
uint semcoin_bought = usd_invested * usd_to_semcoin;            //Total coins bought
equity_semcoin[investor] += semcoin_bought;                     //adding the bought coins to the investor's portfolio
equity_usd[investor] = equity_semcoin[investor]/1000;           //Updating the usd portfolio
total_semcoin_bought += semcoin_bought;                         //Adding it to our varible to control the volume of coins
}


//Function for selling our coin or buying it from the people
function sell_semcoin(address investor, uint coins_sold) external {
    equity_semcoin[investor] -= coins_sold;                     //Decreasing the number of coins investor holds
    equity_usd[investor] = equity_semcoin[investor]/1000;                           //Calculating the portfolio in usd
    total_semcoin_bought -= coins_sold;                         //adding the coins to market or decreasing the number of coins bought
}
=======
pragma solidity ^0.8.18;

contract semcoin_ico{
//we will first define three variables, 1) total number of coins, 2) coin to usd conversion rate, 3) total number of coins bought till now 

uint public max_semcoin = 1000000;        //Max coins that can be circulation
uint public usd_to_semcoin = 1000;         //1 usd equals 1000 semcoin right now
uint public total_semcoin_bought = 0;      //We will initialise to 0 because we haven't sold any


//We will create a mapping to the investor’s address with our coin’s equity and usd. Mapping is like a function, but the data is stored in an array.
mapping (address=> uint) equity_semcoin;              //address is a type in solidity
mapping (address=> uint) equity_usd;                  //mapping will take address as input and return unsigned integer as output with name as equity_usd


//With the help of a modifier we will check if an investor can buy our coin with a certain amount of usd
modifier can_buy_coins(uint usd_invested){
    //we will use a function called require which will check if the condition is true or not
    require (usd_invested * usd_to_semcoin + total_semcoin_bought <= max_semcoin);
    _;  //this tells compiler that the function that is linked with the modifier should only run if the condition is verified.
}

//We will create two functions to check the equity of investor in coin and in usd
function equity_held_semcoin(address investor) external view returns(uint) {
    return equity_semcoin[investor];
}

function equity_held_usd(address investor) external view returns(uint) {
    return equity_usd[investor];
}


//We will now make a function to buy coins in our ether wallet. 
//This function will take two arguments 1st the address of investor and 2nd how much dollar investor want to spend.
//First we will check if they can buy or not
function buy_semcoin(address investor, uint usd_invested) external can_buy_coins(usd_invested){
uint semcoin_bought = usd_invested * usd_to_semcoin;            //Total coins bought
equity_semcoin[investor] += semcoin_bought;                     //adding the bought coins to the investor's portfolio
equity_usd[investor] = equity_semcoin[investor]/1000;           //Updating the usd portfolio
total_semcoin_bought += semcoin_bought;                         //Adding it to our varible to control the volume of coins
}


//Function for selling our coin or buying it from the people
function sell_semcoin(address investor, uint coins_sold) external {
    equity_semcoin[investor] -= coins_sold;                     //Decreasing the number of coins investor holds
    equity_usd[investor] = equity_semcoin[investor]/1000;                           //Calculating the portfolio in usd
    total_semcoin_bought -= coins_sold;                         //adding the coins to market or decreasing the number of coins bought
}
>>>>>>> 517dc3c8e9f7ed8b7298153e90047033ab15ee34
}