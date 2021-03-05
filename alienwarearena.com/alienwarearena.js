var AA={};

AA.delay = 12 * 3600 * 1000;

AA.html = function(p) {
  console.log(new Date().toLocaleString() + ': get page: ' + p);
  setTimeout(()=>AA.html(p), AA.delay);
  $.get(p, function(data) {});
}

AA.pages=[
'https://eu.alienwarearena.com/ucf/Giveaway',
'https://eu.alienwarearena.com/rewards/leaderboard',
'https://eu.alienwarearena.com/ucf/Video',
'https://eu.alienwarearena.com/account',
'https://eu.alienwarearena.com/experiences',
'https://eu.alienwarearena.com/ucf/News'];



AA.start=function() {
  i = 1;
  for (const p of AA.pages) {
    i++;
    const delay = i * 10 * 1000;
    console.log(new Date().toLocaleString() + ': start page: ' + p);
    setTimeout(()=>AA.html(p), delay);
  }

  $('.wrapper').hide();

  return 'started';
}
