//For the project this shall be the main function that will determine the output :


function retirementsavingscalc(income, expenditure, tax, div, roi, inf, retireage, presentage) {
  const principle = (expenditure * 120000) / ((100 * div) - (tax * div));
  const realroi = Math.pow((100 + roi) / (100 + inf), retireage - presentage);
  const savings = principle * (roi - 1) / ((100 + roi) / (100 + inf) - 1);
  const monthlysavings = savings / 12;
  const intpercent = (monthlysavings / income) * 100;
  console.log(`You have to save $${monthlysavings.toFixed(2)} of your monthly income, which is about ${intpercent.toFixed(2)}% to retire at the age of your choice`);
}
