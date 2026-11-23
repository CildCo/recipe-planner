const WEEKDAYS = ["周日", "周一", "周二", "周三", "周四", "周五", "周六"];

function pad(value) {
  return value < 10 ? "0" + value : String(value);
}

function keyOf(date) {
  return date.getFullYear() + "-" + pad(date.getMonth() + 1) + "-" + pad(date.getDate());
}

function parseKey(key) {
  const parts = String(key || "").slice(0, 10).split("-");
  if (parts.length === 3) {
    return new Date(Number(parts[0]), Number(parts[1]) - 1, Number(parts[2]));
  }
  return new Date();
}

function todayKey() {
  return keyOf(new Date());
}

function addDays(key, amount) {
  const date = parseKey(key);
  date.setDate(date.getDate() + amount);
  return keyOf(date);
}

function weekStart(key) {
  const date = parseKey(key || todayKey());
  const offset = (date.getDay() + 6) % 7;
  date.setDate(date.getDate() - offset);
  return keyOf(date);
}

function weekLabel(startKey) {
  const start = parseKey(startKey);
  const end = parseKey(addDays(startKey, 6));
  return start.getMonth() + 1 + "月" + start.getDate() + "日 — " + end.getMonth() + 1 + "月" + end.getDate() + "日";
}

function dayLabel(key) {
  const date = parseKey(key);
  return date.getMonth() + 1 + "月" + date.getDate() + "日";
}

function weekday(key) {
  return WEEKDAYS[parseKey(key).getDay()];
}

function dateLong(key) {
  return dayLabel(key) + " " + weekday(key);
}

function isToday(key) {
  return key === todayKey();
}

function nextDays(count) {
  const rows = [];
  for (let index = 0; index < count; index += 1) {
    const key = addDays(todayKey(), index);
    rows.push({
      key,
      date: key,
      day: parseKey(key).getDate(),
      label: dayLabel(key),
      weekday: weekday(key),
      today: isToday(key),
    });
  }
  return rows;
}

function weekDays(startKey) {
  const rows = [];
  for (let index = 0; index < 7; index += 1) {
    const key = addDays(startKey, index);
    rows.push({
      key,
      date: key,
      day: parseKey(key).getDate(),
      month: parseKey(key).getMonth() + 1,
      label: dayLabel(key),
      weekday: weekday(key),
      today: isToday(key),
    });
  }
  return rows;
}

module.exports = {
  WEEKDAYS,
  pad,
  keyOf,
  parseKey,
  todayKey,
  addDays,
  weekStart,
  weekLabel,
  dayLabel,
  weekday,
  dateLong,
  isToday,
  nextDays,
  weekDays,
};
