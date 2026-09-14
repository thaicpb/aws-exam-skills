/* Shared state machine used by the HTML UI and Node tests. */
(function (root) {
  'use strict';
  class QuizEngine {
    constructor(exam, now = () => Date.now()) {
      this.exam = exam;
      this.now = now;
      this.answers = exam.questions.map(() => new Set());
      this.confirmed = exam.questions.map(() => false);
      this.flags = exam.questions.map(() => false);
      this.started = false;
      this.finished = false;
      this.deadline = null;
      this.reason = null;
    }
    start() {
      if (this.started) return;
      this.started = true;
      if (this.exam.mode === 'exam') this.deadline = this.now() + this.exam.duration_minutes * 60000;
    }
    tick() {
      if (this.started && !this.finished && this.deadline !== null && this.now() >= this.deadline) {
        this.finished = true;
        this.reason = 'timeout';
      }
      return this.finished;
    }
    remainingSeconds() {
      return this.deadline === null ? null : Math.max(0, Math.ceil((this.deadline - this.now()) / 1000));
    }
    select(index, id) {
      this.tick();
      const question = this.exam.questions[index];
      if (!this.started || this.finished || !question ||
          (this.exam.mode === 'practice' && this.confirmed[index]) ||
          !question.options.some(option => option.id === id)) return false;
      if (question.type === 'single') this.answers[index] = new Set([id]);
      else if (this.answers[index].has(id)) this.answers[index].delete(id);
      else if (this.answers[index].size < question.correct_option_ids.length) this.answers[index].add(id);
      else return false;
      return true;
    }
    confirm(index) {
      this.tick();
      if (!this.started || this.finished || this.exam.mode !== 'practice' || this.confirmed[index] ||
          !this.exam.questions[index] || this.answers[index].size !== this.exam.questions[index].correct_option_ids.length) return false;
      this.confirmed[index] = true;
      return true;
    }
    toggleFlag(index) {
      this.tick();
      if (!this.started || this.finished || !this.exam.questions[index]) return false;
      this.flags[index] = !this.flags[index];
      return true;
    }
    finish() {
      this.tick();
      if (!this.started || this.finished) return false;
      this.finished = true;
      this.reason = 'submitted';
      return true;
    }
    canReview(index) {
      return this.finished || (this.exam.mode === 'practice' && this.confirmed[index]);
    }
    isCorrect(index) {
      const correct = this.exam.questions[index].correct_option_ids;
      return (this.exam.mode === 'exam' || this.confirmed[index]) &&
        this.answers[index].size === correct.length && correct.every(id => this.answers[index].has(id));
    }
    incompleteCount() {
      return this.exam.questions.filter((q, i) => this.exam.mode === 'practice' ? !this.confirmed[i] : this.answers[i].size !== q.correct_option_ids.length).length;
    }
    score() {
      if (this.exam.mode === 'exam' && !this.finished) return null;
      const domains = Array.from({length: 4}, (_, index) => ({domain: index + 1, correct: 0, total: 0}));
      let correct = 0;
      this.exam.questions.forEach((q, i) => {
        domains[q.primary_domain - 1].total++;
        if (this.isCorrect(i)) { correct++; domains[q.primary_domain - 1].correct++; }
      });
      return {correct, total: this.exam.questions.length, domains};
    }
  }
  if (typeof module !== 'undefined' && module.exports) module.exports = QuizEngine;
  else root.QuizEngine = QuizEngine;
})(typeof globalThis !== 'undefined' ? globalThis : this);
