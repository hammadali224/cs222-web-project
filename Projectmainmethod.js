//For the project this shall be the main function that will determine the output :


function retirementsavingscalc(income, expenditure, tax, div, roi, inf, retireage, presentage) {
let principle = (expenditure * 120000) / ((100 * div) - (tax * div));
let realroi = (100 + roi) / (100 + inf);
let num = realroi;
let n = retireage - presentage;
for (let i = 1; i < n; i++) {
realroi = realroi * num;
}
let geometricprogression = (roi - 1) / (num - 1);
let savings = principle / geometricprogression;
let monthlysavings = savings / 12;
let intpercent = (monthlysavings / income) * 100;
console.log(`You have to save $${monthlysavings.toFixed(2)} of your monthly income, which is about ${intpercent.toFixed(2)}% to retire at the age of your choice`);
}
