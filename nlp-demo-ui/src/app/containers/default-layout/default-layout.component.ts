import { Component } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-dashboard",
  templateUrl: "./default-layout.component.html",
  styleUrls: ["./default-layout.component.css"]
})
export class DefaultLayoutComponent {
  demo = "translate";
  lang = "Bulgarian";
  words = "приятел";
  wordResp = [];
  error = "";

  fisrtLang = "Spanish";
  secondLang = "Bulgarian";
  constructor(private http: HttpClient) {}

  setDemo(type) {
    this.demo = type;
  }

  toggleLang() {
    this.wordResp = [];
    if (this.lang === "Bulgarian") {
      this.lang = "Spanish";
      this.words = "amigo";
    } else {
      this.lang = "Bulgarian";
      this.words = "приятел";
    }
  }

  callWv() {
    this.error = null;
    const body = {
      positive: this.words.split(" "),
      negative: []
    };
    const httpOptions = {
      headers: new HttpHeaders({
        "Content-Type": "application/json;charset=UTF-8"
      })
    };

    let port = 10001;
    if (this.lang === "Spanish") {
      port = 10002;
    }

    const url = "http://localhost:" + port + "/words";
    this.http.post(url, body, httpOptions).subscribe(
      res => {
        this.wordResp = [];
        for (const w of Object.keys(res["words"])) {
          this.wordResp.push(w);
        }
      },
      err => {
        console.log(err);
        this.error = err.message;
      }
    );
  }

  switchLang() {
    const temp = this.fisrtLang;
    this.fisrtLang = this.secondLang;
    this.secondLang = temp;
  }

  callOtherVector() {
    this.http
  }
}
