const LOAN_TYPE_RATES = {
  'Normal Loan': { monthly: 1.0, annual: 12.0 },
  'Emergency Loan': { monthly: 1.3, annual: 15.6 },
  'School Fees Loan': { monthly: 1.15, annual: 13.8 },
  'M-Cash Loan': { monthly: 5.0, annual: 60.0 },
  'Super Loan': { monthly: 1.2, annual: 14.4 },
  'M-Cash': { monthly: 5.0, annual: 60.0 }
};

let portfolioData = [];

function nav(page, el) {
  document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
  el.classList.add('active');
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById(`page-${page}`).classList.add('active');
  document.getElementById('page-title').textContent = page === 'dashboard' ? 'Portfolio Dashboard' :
    page === 'calculator' ? 'Loan Risk Calculator' :
    page === 'lookup' ? 'Member Lookup' : 'Risk Methodology';
  if (page === 'dashboard') renderDashboard();
}

function formatMoney(value) {
  return typeof value === 'number' ? value.toLocaleString('en-KE', { maximumFractionDigits: 0 }) : '0';
}

function formatDate(value) {
  if (!value) return '—';
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return String(value);
  return d.toLocaleDateString('en-KE', { year: 'numeric', month: 'short', day: 'numeric' });
}

function normalizeSearch(value) {
  return String(value || '').replace(/[^0-9+]/g, '').trim();
}

function loadData() {
  fetch('data/members.json')
    .then(response => response.json())
    .then(data => {
      portfolioData = data;
      document.getElementById('summary-members').textContent = `${new Set(data.map(item => item.member_no)).size} members`;
      document.getElementById('summary-portfolio').textContent = `${formatMoney(data.reduce((sum, item) => sum + (item.balance || 0), 0))} portfolio`;
      fillLoanTypes();
      renderDashboard();
    })
    .catch(() => {
      document.getElementById('summary-members').textContent = 'Unable to load dataset';
      document.getElementById('summary-portfolio').textContent = '—';
    });
}

function fillLoanTypes() {
  const select = document.getElementById('c-type');
  select.innerHTML = '';
  Object.keys(LOAN_TYPE_RATES).forEach(type => {
    const option = document.createElement('option');
    option.textContent = type;
    option.value = type;
    select.append(option);
  });
  select.addEventListener('change', autoRate);
  autoRate();
}

function autoRate() {
  const type = document.getElementById('c-type').value;
  const rate = LOAN_TYPE_RATES[type] || { monthly: 0, annual: 0 };
  document.getElementById('c-rate').value = rate.annual.toFixed(2);
  document.getElementById('monthly-rate').textContent = `${rate.monthly.toFixed(2)}% monthly`;
}

function renderDashboard() {
  const data = portfolioData;
  if (!data.length) return;
  const totalBalance = data.reduce((sum, item) => sum + (item.balance || 0), 0);
  const days = item => item.days_in_arrears || 0;
  const par30 = data.filter(item => days(item) > 30).reduce((sum, item) => sum + (item.balance || 0), 0);
  const par90 = data.filter(item => days(item) > 90).reduce((sum, item) => sum + (item.balance || 0), 0);
  const performing = data.filter(item => item.classification === 'Performing').reduce((sum, item) => sum + (item.balance || 0), 0);
  const watch = data.filter(item => /Watch/i.test(item.classification)).reduce((sum, item) => sum + (item.balance || 0), 0);
  const substandard = data.filter(item => /Substandard/i.test(item.classification)).reduce((sum, item) => sum + (item.balance || 0), 0);
  const doubtful = data.filter(item => /Doubtful/i.test(item.classification)).reduce((sum, item) => sum + (item.balance || 0), 0);
  const loss = data.filter(item => /Loss/i.test(item.classification)).reduce((sum, item) => sum + (item.balance || 0), 0);
  const activeMembers = new Set(data.map(item => item.member_no)).size;
  const totalLoans = data.length;
  const average = totalBalance / Math.max(totalLoans, 1);
  const collectionRate = totalBalance ? Math.max(0, 100 - ((par30 / totalBalance) * 100).toFixed(1)) : 0;

  document.getElementById('metric-portfolio').textContent = `KSh ${formatMoney(totalBalance)}`;
  document.getElementById('metric-par30').textContent = `${((par30 / Math.max(totalBalance,1)) * 100).toFixed(1)}%`;
  document.getElementById('metric-par90').textContent = `${((par90 / Math.max(totalBalance,1)) * 100).toFixed(1)}%`;
  document.getElementById('metric-collection').textContent = `${collectionRate.toFixed(1)}%`;
  document.getElementById('pool-products').textContent = `${totalLoans} loans`;
  document.getElementById('pool-balance').textContent = `KSh ${formatMoney(totalBalance)}`;
  document.getElementById('pool-members').textContent = `${activeMembers} members`;
  document.getElementById('pool-average').textContent = `KSh ${formatMoney(average)}`;

  document.getElementById('bar-performing').style.width = `${Math.min(100, (performing / Math.max(totalBalance, 1)) * 100)}%`;
  document.getElementById('bar-watch').style.width = `${Math.min(100, (watch / Math.max(totalBalance, 1)) * 100)}%`;
  document.getElementById('bar-substandard').style.width = `${Math.min(100, (substandard / Math.max(totalBalance, 1)) * 100)}%`;
  document.getElementById('bar-doubtful').style.width = `${Math.min(100, (doubtful / Math.max(totalBalance, 1)) * 100)}%`;
  document.getElementById('bar-loss').style.width = `${Math.min(100, (loss / Math.max(totalBalance, 1)) * 100)}%`;

  document.getElementById('pct-performing').textContent = `${((performing / Math.max(totalBalance, 1)) * 100).toFixed(0)}%`;
  document.getElementById('pct-watch').textContent = `${((watch / Math.max(totalBalance, 1)) * 100).toFixed(0)}%`;
  document.getElementById('pct-substandard').textContent = `${((substandard / Math.max(totalBalance, 1)) * 100).toFixed(0)}%`;
  document.getElementById('pct-doubtful').textContent = `${((doubtful / Math.max(totalBalance, 1)) * 100).toFixed(0)}%`;
  document.getElementById('pct-loss').textContent = `${((loss / Math.max(totalBalance, 1)) * 100).toFixed(0)}%`;
  document.getElementById('amt-performing').textContent = `KSh ${formatMoney(performing)}`;
  document.getElementById('amt-watch').textContent = `KSh ${formatMoney(watch)}`;
  document.getElementById('amt-substandard').textContent = `KSh ${formatMoney(substandard)}`;
  document.getElementById('amt-doubtful').textContent = `KSh ${formatMoney(doubtful)}`;
  document.getElementById('amt-loss').textContent = `KSh ${formatMoney(loss)}`;

  const top = data.sort((a, b) => (b.balance || 0) - (a.balance || 0)).slice(0, 8);
  const tbody = document.querySelector('#top-risk-table tbody');
  tbody.innerHTML = top.map(item => `<tr>
      <td style="font-family:var(--font-mono)">${item.member_no}</td>
      <td>${item.full_name}</td>
      <td>${item.loan_name}</td>
      <td style="font-family:var(--font-mono)">KSh ${formatMoney(item.balance)}</td>
      <td style="font-family:var(--font-mono)">${item.days_in_arrears || 0}</td>
      <td><span class="badge ${item.classification.toLowerCase().includes('loss') ? 'badge-loss' : item.classification.toLowerCase().includes('doubt') ? 'badge-doubt' : item.classification.toLowerCase().includes('substandard') ? 'badge-sub' : item.classification.toLowerCase().includes('watch') ? 'badge-watch' : 'badge-ok'}">${item.classification}</span></td>
    </tr>`).join('');
}

function calcRisk() {
  const amount = Number(document.getElementById('c-amount').value);
  const term = Number(document.getElementById('c-term').value);
  const deposits = Number(document.getElementById('c-deposits').value);
  const arrears = Number(document.getElementById('c-arrears').value);
  const annual = Number(document.getElementById('c-rate').value);
  const monthlyRate = annual / 12 / 100;
  if (!amount || !term || !annual) return;
  const emi = monthlyRate === 0 ? amount / term : amount * monthlyRate * Math.pow(1 + monthlyRate, term) / (Math.pow(1 + monthlyRate, term) - 1);
  const ltd = deposits ? (amount / deposits) * 100 : 0;
  const riskScore = Math.min(100, Math.max(0, (ltd * 0.6) + (arrears * 0.4)));
  const verdict = riskScore < 35 ? 'Healthy' : riskScore < 60 ? 'Monitor' : 'Elevated';
  const verdictClass = riskScore < 35 ? 'low' : riskScore < 60 ? 'medium' : 'high';
  const verdictText = riskScore < 35 ? 'Loan has conservative exposure and good coverage.' : riskScore < 60 ? 'Review member deposit cover and repayment history.' : 'High exposure; follow up before disbursement.';

  document.getElementById('r-emi').textContent = `KSh ${formatMoney(Math.round(emi))}`;
  document.getElementById('r-ltd').textContent = `${ltd.toFixed(1)}%`;
  document.getElementById('r-rate').textContent = `${annual.toFixed(2)}%`;
  document.getElementById('r-verdict').textContent = verdict;
  const verdictCard = document.getElementById('r-verdict-card');
  verdictCard.className = `risk-verdict ${verdictClass}`;
  document.getElementById('verdict-level').textContent = verdict;
  document.getElementById('verdict-text').textContent = verdictText;
  document.getElementById('calc-result').style.display = 'block';
}

function resetCalc() {
  document.getElementById('c-amount').value = 200000;
  document.getElementById('c-term').value = 24;
  document.getElementById('c-deposits').value = 80000;
  document.getElementById('c-arrears').value = 0;
  autoRate();
  document.getElementById('calc-result').style.display = 'none';
}

function searchMember() {
  const term = normalizeSearch(document.getElementById('lookup-input').value);
  const message = document.getElementById('lookup-message');
  const results = document.getElementById('lookup-results');
  const tbody = document.querySelector('#lookup-table tbody');
  const profile = document.getElementById('lookup-profile');
  message.innerHTML = '';
  tbody.innerHTML = '';
  results.style.display = 'none';
  if (!term) {
    message.innerHTML = '<div class="empty-state"><p>Please enter a member number, phone number or account ID.</p></div>';
    return;
  }
  const normalizedTerm = term.replace(/^\+/, '').replace(/^254/, '');
  const matches = portfolioData.filter(item => {
    const member = item.member_no.replace(/^0+/, '');
    const mobile = (item.mobile_no || '').replace(/[^0-9]/g, '');
    const account = (item.account_id || '').replace(/^0+/, '');
    return member === normalizedTerm || mobile.endsWith(normalizedTerm) || account === normalizedTerm;
  });

  if (!matches.length) {
    message.innerHTML = `<div class="empty-state"><p>No matching member loan records found in the current dataset.</p></div>`;
    return;
  }

  results.style.display = 'block';
  const member = matches[0];
  const uniqueLoans = matches;
  profile.innerHTML = `
    <div class="profile-avatar">${member.full_name ? member.full_name.split(' ').map(p => p[0]).join('').slice(0,2).toUpperCase() : 'R'}</div>
    <div>
      <div class="card-title">${member.full_name || 'Unknown member'}</div>
      <div class="profile-stat-row"><span class="profile-stat-label">Member No.</span><span class="profile-stat-val">${member.member_no}</span></div>
      <div class="profile-stat-row"><span class="profile-stat-label">Account ID</span><span class="profile-stat-val">${member.account_id}</span></div>
      <div class="profile-stat-row"><span class="profile-stat-label">Phone</span><span class="profile-stat-val">${member.mobile_no || '—'}</span></div>
      <div class="profile-stat-row"><span class="profile-stat-label">Total loans</span><span class="profile-stat-val">${uniqueLoans.length}</span></div>
    </div>
  `;

  tbody.innerHTML = uniqueLoans.map(item => `
    <tr>
      <td>${item.loan_name}</td>
      <td>KSh ${formatMoney(item.balance)}</td>
      <td>${item.days_in_arrears || 0}</td>
      <td>${item.annual_rate ? item.annual_rate.toFixed(1) : '—'}%</td>
      <td><span class="badge ${item.classification.toLowerCase().includes('loss') ? 'badge-loss' : item.classification.toLowerCase().includes('doubt') ? 'badge-doubt' : item.classification.toLowerCase().includes('substandard') ? 'badge-sub' : item.classification.toLowerCase().includes('watch') ? 'badge-watch' : 'badge-ok'}">${item.classification}</span></td>
      <td>${formatDate(item.loan_maturity)}</td>
    </tr>
  `).join('');
  document.getElementById('lookup-count').textContent = `${uniqueLoans.length} loans`;
}

document.addEventListener('DOMContentLoaded', () => {
  loadData();
  autoRate();
});
