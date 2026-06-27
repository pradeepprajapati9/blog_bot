"""Generate free calculator tools (static HTML+JS) into docs/tools/.

These rank for huge-volume searches like 'EMI calculator', 'SIP calculator',
'age calculator' and earn AdSense on recurring traffic. Run once:
  python make_tools.py
"""
import html
import config
import render

TOOLS_DIR = config.DOCS_DIR / "tools"
TOOLS_DIR.mkdir(exist_ok=True)

def _head(title, desc):
    # reuse the blog's external-CSS head, with paths relative to /tools
    return render._head(title, desc, css_path="../style.css",
                        home="../index.html", tools="index.html")


FOOT = ('<p style="margin-top:24px"><a href="index.html">&larr; All calculators</a></p>'
        '</div></main>' + render.FOOT)


def page(slug, title, desc, body):
    head = (_head(title, desc) +
            f'<main class="wrap"><div class="tool">'
            f'<h1 class="title">{html.escape(title)}</h1>')
    (TOOLS_DIR / f"{slug}.html").write_text(head + body + FOOT, "utf-8")


# ---------------- calculators ----------------
EMI = """
<p>Calculate your monthly loan EMI, total interest and total payment instantly.</p>
<label>Loan Amount (Rs.)</label><input id="p" type="number" value="500000">
<label>Interest Rate (% per year)</label><input id="r" type="number" value="9" step="0.1">
<label>Tenure (years)</label><input id="y" type="number" value="5">
<button onclick="emi()">Calculate EMI</button>
<div id="out" class="result" style="display:none"></div>
<script>
function fmt(n){return '₹'+Math.round(n).toLocaleString('en-IN')}
function emi(){var P=+p.value,r=(+document.getElementById('r').value)/12/100,
n=(+document.getElementById('y').value)*12;
var e=r? P*r*Math.pow(1+r,n)/(Math.pow(1+r,n)-1) : P/n;
var tot=e*n, intr=tot-P;
out.style.display='block';
out.innerHTML='Monthly EMI: <b>'+fmt(e)+'</b><br>Total Interest: '+fmt(intr)+
'<br>Total Payment: '+fmt(tot);}
emi();
</script>"""

SIP = """
<p>See how much your monthly SIP investment can grow over time.</p>
<label>Monthly Investment (Rs.)</label><input id="m" type="number" value="5000">
<label>Expected Return (% per year)</label><input id="er" type="number" value="12" step="0.1">
<label>Time Period (years)</label><input id="ty" type="number" value="10">
<button onclick="sip()">Calculate</button>
<div id="o" class="result" style="display:none"></div>
<script>
function f2(n){return '₹'+Math.round(n).toLocaleString('en-IN')}
function sip(){var P=+m.value,i=(+er.value)/12/100,n=(+ty.value)*12;
var fv=i? P*(Math.pow(1+i,n)-1)/i*(1+i) : P*n;
var inv=P*n;
o.style.display='block';
o.innerHTML='Maturity Value: <b>'+f2(fv)+'</b><br>Invested: '+f2(inv)+
'<br>Estimated Gains: '+f2(fv-inv);}
sip();
</script>"""

AGE = """
<p>Find your exact age in years, months and days from your date of birth.</p>
<label>Date of Birth</label><input id="dob" type="date">
<button onclick="age()">Calculate Age</button>
<div id="ao" class="result" style="display:none"></div>
<script>
function age(){if(!dob.value){return}
var b=new Date(dob.value),t=new Date();
var y=t.getFullYear()-b.getFullYear(),m=t.getMonth()-b.getMonth(),d=t.getDate()-b.getDate();
if(d<0){m--;d+=new Date(t.getFullYear(),t.getMonth(),0).getDate()}
if(m<0){y--;m+=12}
ao.style.display='block';
ao.innerHTML='Your age: <b>'+y+' years, '+m+' months, '+d+' days</b>';}
</script>"""

GST = """
<p>Add or remove GST from any amount. Supports 5%, 12%, 18% and 28% slabs.</p>
<label>Amount (Rs.)</label><input id="amt" type="number" value="1000">
<div class="row"><div><label>GST Rate (%)</label>
<select id="gr"><option>5</option><option selected>18</option><option>12</option>
<option>28</option></select></div>
<div><label>Type</label><select id="gt"><option value="add">Add GST</option>
<option value="rem">Remove GST</option></select></div></div>
<button onclick="gst()">Calculate</button>
<div id="go" class="result" style="display:none"></div>
<script>
function f3(n){return '₹'+(Math.round(n*100)/100).toLocaleString('en-IN')}
function gst(){var a=+amt.value,r=+gr.value;
var base,tax,total;
if(gt.value=='add'){base=a;tax=a*r/100;total=a+tax}
else{base=a*100/(100+r);tax=a-base;total=a}
go.style.display='block';
go.innerHTML='GST Amount: <b>'+f3(tax)+'</b><br>Base Amount: '+f3(base)+
'<br>Total: '+f3(total);}
gst();
</script>"""

PCT = """
<p>Quick percentage calculator for everyday maths.</p>
<label>What is X% of Y?</label>
<div class="row"><div><input id="x" type="number" value="20" placeholder="X%"></div>
<div><input id="y2" type="number" value="1500" placeholder="Y"></div></div>
<button onclick="pct()">Calculate</button>
<div id="po" class="result" style="display:none"></div>
<script>
function pct(){var v=(+x.value)/100*(+y2.value);
po.style.display='block';
po.innerHTML=x.value+'% of '+y2.value+' = <b>'+(Math.round(v*100)/100)+'</b>';}
pct();
</script>"""


TOOLS = [
    ("emi-calculator", "EMI Calculator - Loan EMI, Interest & Total Payment",
     "Free EMI calculator: find your monthly loan EMI, total interest and total payment for home, car or personal loans.", EMI),
    ("sip-calculator", "SIP Calculator - Mutual Fund Returns Estimator",
     "Free SIP calculator: estimate the maturity value and returns of your monthly mutual fund SIP investment.", SIP),
    ("age-calculator", "Age Calculator - Find Your Exact Age",
     "Free age calculator: find your exact age in years, months and days from your date of birth.", AGE),
    ("gst-calculator", "GST Calculator - Add or Remove GST (India)",
     "Free GST calculator for India: add or remove 5%, 12%, 18% or 28% GST from any amount instantly.", GST),
    ("percentage-calculator", "Percentage Calculator - Easy % Maths",
     "Free percentage calculator: quickly find what X percent of Y is.", PCT),
]


def build():
    render.write_css()                      # ensure the shared theme exists
    for slug, title, desc, body in TOOLS:
        page(slug, title, desc, body)
    cards = "".join(
        f'<div class="card"><a href="{s}.html">{html.escape(t)}</a></div>'
        for s, t, d, b in TOOLS)
    idx = (_head("Free Online Tools & Calculators",
                 "Free calculators: EMI, SIP, Age, GST and Percentage - fast and accurate.")
           + '<main class="wrap"><h1 class="title">Free Tools &amp; Calculators</h1>'
           + cards + '</main>' + render.FOOT)
    (TOOLS_DIR / "index.html").write_text(idx, "utf-8")
    print(f"Built {len(TOOLS)} tools + index in {TOOLS_DIR}")


if __name__ == "__main__":
    build()
