var AA = {};

AA.index = 0;

AA.pages = [
'/ucf/Giveaway',
'/rewards/leaderboard',
'/ucf/Video',
'/account',
'/experiences',
'/ucf/News',
'/rewards'];

AA.lastPage = '';

AA.delay = function() {
 return 3600 * 1000 * 24 / AA.pages.length;
}

AA.html = function() {
  const p = AA.pages[AA.index % AA.pages.length];
  console.log(new Date().toLocaleString() + ': get page[' + AA.index + ']: ' + p);
  setTimeout(()=>AA.html(), AA.delay());
  AA.index++;
  $.get(p, AA.logResult);
}

AA.logResult = function(data) {
  console.log(data.substring(0, 1500));
  AA.lastPage = data;
}

AA.start = function() {

  AA.html();

  $('.wrapper').hide();

  return 'started';
}
