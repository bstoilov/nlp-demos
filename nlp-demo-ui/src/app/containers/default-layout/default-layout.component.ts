import { Component } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http";

@Component({
  selector: "app-dashboard",
  templateUrl: "./default-layout.component.html",
  styleUrls: ["./default-layout.component.css"]
})
export class DefaultLayoutComponent {
  demo = "clusters";
  words = "приятел";
  wordResp = [];
  error = "";

  group = "ябълка морков целина домат картоф";
  url =
    "https://gotvach.bg/n5-108642-%D0%A2%D1%8A%D0%BD%D0%BA%D0%BE%D1%81%D1%82%D0%B8_%D0%BF%D1%80%D0%B8_%D0%BF%D1%80%D0%B8%D0%B3%D0%BE%D1%82%D0%B2%D1%8F%D0%BD%D0%B5_%D0%BD%D0%B0_%D1%89%D1%80%D0%B0%D1%83%D1%81%D0%BE%D0%B2%D0%BE%D1%82%D0%BE_%D0%BC%D0%B5%D1%81%D0%BE";

  clusterRes = [];

  first = "пловдив";
  second = "варна бургас";
  similarity;
  constructor(private http: HttpClient) {}

  setDemo(type) {
    this.demo = type;
  }

  callWv() {
    this.error = null;
    const body = {
      positive: this.words.toLocaleLowerCase().split(" "),
      negative: []
    };
    const httpOptions = {
      headers: new HttpHeaders({
        "Content-Type": "application/json;charset=UTF-8"
      })
    };

    const url = "http://localhost:10001/words";
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

  callClusters() {
    this.error = null;
    const httpOptions = {
      headers: new HttpHeaders({
        "Content-Type": "application/json;charset=UTF-8"
      })
    };
    const body = {
      group: this.group,
      url: this.url
    };
    const url = "http://localhost:10001/belong";
    this.http.post(url, body, httpOptions).subscribe(
      res => {
        this.clusterRes = res["items"];
      },
      err => {
        console.log(err);
        this.error = err.message;
      }
    );
  }

  callSimilarity() {
    this.error = null;
    const httpOptions = {
      headers: new HttpHeaders({
        "Content-Type": "application/json;charset=UTF-8"
      })
    };
    const body = {
      first: this.first,
      second: this.second
    };
    const url = "http://localhost:10001/similarity";
    this.http.post(url, body, httpOptions).subscribe(
      res => {
        this.similarity = res["similarity"];
      },
      err => {
        console.log(err);
        this.error = err.message;
      }
    );
  }

  getSim() {
    if (this.similarity) {
      return Math.floor(this.similarity * 100);
    }
    return "";
  }
}
