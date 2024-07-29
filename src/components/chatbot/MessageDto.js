// src/models/MessageDto.js
export class MessageDto {
    constructor(isUser, content, color, isSuggested) {
      this.isUser = isUser;
      this.content = content;
      this.color = color;
      this.isSuggested = isSuggested;
    }
  }
  