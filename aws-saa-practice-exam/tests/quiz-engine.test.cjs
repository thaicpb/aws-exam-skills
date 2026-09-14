const {test} = require('node:test');
const assert = require('node:assert/strict');
const QuizEngine = require('../assets/quiz-engine.js');
function exam(mode = 'practice') {
  return {mode, duration_minutes: 1, questions: [
    {type: 'single', primary_domain: 1, options: ['A','B','C','D'].map(id => ({id})), correct_option_ids: ['B']},
    {type: 'multiple', primary_domain: 2, options: ['A','B','C','D','E'].map(id => ({id})), correct_option_ids: ['A','C']}
  ]};
}
test('cannot answer before start and cannot restart timer', () => {
  let now=0; const q=new QuizEngine(exam('exam'), () => now);
  assert.equal(q.select(0,'B'),false); q.start(); now=10000; q.start(); assert.equal(q.deadline,60000);
});
test('practice requires exact selection count, locks answer, does not double count', () => {
  const q=new QuizEngine(exam()); q.start(); assert.equal(q.confirm(0),false);
  q.select(0,'B'); assert.equal(q.confirm(0),true); assert.equal(q.confirm(0),false);
  assert.equal(q.select(0,'A'),false); assert.equal(q.score().correct,1);
});
test('multiple set equality independent of order; capped selections can be changed', () => {
  const q=new QuizEngine(exam()); q.start(); q.select(1,'C'); assert.equal(q.confirm(1),false);
  q.select(1,'A'); assert.equal(q.select(1,'B'),false); q.confirm(1); assert.equal(q.isCorrect(1),true);
});
test('partial and wrong combination earn no partial credit', () => {
  for (const answers of [['A'],['A','B'],[]]) {
    const q=new QuizEngine(exam('exam')); q.start(); answers.forEach(id=>q.select(1,id)); q.finish();
    assert.equal(q.score().correct,0);
  }
});
test('exam hides scoring and review until submitted', () => {
  const q=new QuizEngine(exam('exam')); q.start(); q.select(0,'B');
  assert.equal(q.score(),null); assert.equal(q.canReview(0),false); assert.equal(q.confirm(0),false);
  q.finish(); assert.equal(q.score().correct,1); assert.equal(q.canReview(0),true);
});
test('selections and flags persist while other questions are answered', () => {
  const q=new QuizEngine(exam('exam')); q.start(); q.select(0,'B'); q.toggleFlag(0); q.select(1,'C');
  assert.deepEqual([...q.answers[0]],['B']); assert.equal(q.flags[0],true); q.select(0,'D');
  assert.deepEqual([...q.answers[0]],['D']); assert.deepEqual([...q.answers[1]],['C']);
});
test('timeout uses elapsed time and blocks a late answer before interval fires', () => {
  let now=0; const q=new QuizEngine(exam('exam'),()=>now); q.start(); q.select(0,'B'); now=60000;
  assert.equal(q.select(1,'A'),false); assert.equal(q.reason,'timeout'); assert.equal(q.score().correct,1);
  assert.equal(q.remainingSeconds(),0); assert.equal(q.finish(),false);
});
test('submission freezes answers and counts all domains including empty ones', () => {
  const q=new QuizEngine(exam('exam')); q.start(); q.select(0,'B'); q.finish();
  assert.equal(q.select(0,'A'),false); assert.equal(q.toggleFlag(0),false);
  assert.deepEqual(q.score().domains,[{domain:1,correct:1,total:1},{domain:2,correct:0,total:1},{domain:3,correct:0,total:0},{domain:4,correct:0,total:0}]);
});
test('unconfirmed practice answers count as incorrect on early submit', () => {
  const q=new QuizEngine(exam()); q.start(); q.select(0,'B'); q.finish(); assert.equal(q.score().correct,0);
});
test('practice has no timer, incomplete count tracks confirmation', () => {
  let now=0; const q=new QuizEngine(exam(),()=>now); q.start(); now=9999999;
  assert.equal(q.tick(),false); assert.equal(q.remainingSeconds(),null); q.select(0,'B'); q.confirm(0);
  assert.equal(q.incompleteCount(),1);
});
