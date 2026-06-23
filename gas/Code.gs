/**
 * IPA TTS proxy — OpenAI speech via GAS, cached on Google Drive.
 *
 * Script property: OPENAI_API_KEY
 * Deploy as Web App (Execute as: Me, Who has access: Anyone).
 */

const FOLDER_NAME = 'IPA-TTS-Audio';
const TTS_MODEL = 'gpt-4o-mini-tts';
const TTS_VOICE = 'alloy';

function getFolder_() {
  const folders = DriveApp.getFoldersByName(FOLDER_NAME);
  if (folders.hasNext()) return folders.next();
  return DriveApp.createFolder(FOLDER_NAME);
}

function fileNameForWord_(word) {
  return String(word).toLowerCase().replace(/[^a-z0-9]/g, '_') + '.mp3';
}

function getAudioFromDrive_(word) {
  const folder = getFolder_();
  const name = fileNameForWord_(word);
  const files = folder.getFilesByName(name);
  if (!files.hasNext()) return null;
  return files.next().getBlob();
}

function fetchFromOpenAI_(word) {
  const key = PropertiesService.getScriptProperties().getProperty('OPENAI_API_KEY');
  if (!key) throw new Error('OPENAI_API_KEY is not set in Script Properties');

  const res = UrlFetchApp.fetch('https://api.openai.com/v1/audio/speech', {
    method: 'post',
    headers: {
      Authorization: 'Bearer ' + key,
      'Content-Type': 'application/json',
    },
    payload: JSON.stringify({
      model: TTS_MODEL,
      input: word,
      voice: TTS_VOICE,
    }),
    muteHttpExceptions: true,
  });

  if (res.getResponseCode() !== 200) {
    throw new Error('OpenAI ' + res.getResponseCode() + ': ' + res.getContentText().slice(0, 200));
  }
  return res.getBlob();
}

function saveToDrive_(word, blob) {
  const folder = getFolder_();
  const name = fileNameForWord_(word);
  const existing = folder.getFilesByName(name);
  while (existing.hasNext()) existing.next().setTrashed(true);
  folder.createFile(blob.setName(name));
}

function jsonResponse_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function doGet(e) {
  try {
    const word = String((e && e.parameter && e.parameter.word) || '').trim();
    if (!word || !/^[a-zA-Z][a-zA-Z'-]*$/.test(word)) {
      return jsonResponse_({ ok: false, error: 'Invalid or missing word parameter' });
    }

    let blob = getAudioFromDrive_(word);
    let source = 'drive';
    if (!blob) {
      blob = fetchFromOpenAI_(word);
      saveToDrive_(word, blob);
      source = 'openai';
    }

    return jsonResponse_({
      ok: true,
      word: word,
      source: source,
      mimeType: blob.getContentType() || 'audio/mpeg',
      audio: Utilities.base64Encode(blob.getBytes()),
    });
  } catch (err) {
    return jsonResponse_({ ok: false, error: String(err.message || err) });
  }
}
