/**
 * INTELLECT HOMES - 2026 LUXURY BUILDER CORE LOGIC
 * High-conversion interactive tools, calculators, modal controls
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initCalculator();
  initDesignFilters();
  initModals();
  initFAQ();
  initConsultationForm();
  initVIPConcierge();
  initRoomInspector();
});

/* ==========================================================================
   1. NAVBAR & SCROLL EFFECTS
   ========================================================================== */
function initNavbar() {
  const header = document.querySelector('.site-header');
  const mobileToggle = document.querySelector('.mobile-menu-btn');
  const navMenu = document.querySelector('.nav-menu');

  if (header) {
    window.addEventListener('scroll', () => {
      if (window.scrollY > 40) {
        header.classList.add('scrolled');
      } else {
        header.classList.remove('scrolled');
      }
    });
  }

  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      const icon = mobileToggle.querySelector('svg');
      if (icon) {
        // Toggle simple state
        mobileToggle.setAttribute('aria-expanded', navMenu.classList.contains('open'));
      }
    });

    // Close when clicking a nav link on mobile
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
      });
    });
  }
}

/* ==========================================================================
   2. INTERACTIVE BUILD COST CALCULATOR
   ========================================================================== */
function initCalculator() {
  const calcContainer = document.querySelector('.calculator-wrapper');
  if (!calcContainer) return;

  // Base state
  const state = {
    projectType: 'kdr', // 'kdr', 'custom', 'granny', 'dual'
    sizeConfig: 'double-large', // 'single-mid', 'single-large', 'double-mid', 'double-large', 'granny-60'
    finishTier: 'signature', // 'signature', 'prestige'
    includeDemo: true,
    includeLandscaping: true
  };

  // Pricing matrix (Melbourne 2026 typical luxury builder rates)
  const basePrices = {
    'kdr': {
      'single-mid': { signature: 460000, prestige: 540000, size: '26 Squares (241 m²)', time: '8-10 Months' },
      'single-large': { signature: 540000, prestige: 630000, size: '32 Squares (297 m²)', time: '9-11 Months' },
      'double-mid': { signature: 680000, prestige: 790000, size: '38 Squares (353 m²)', time: '11-13 Months' },
      'double-large': { signature: 840000, prestige: 990000, size: '48 Squares (446 m²)', time: '12-15 Months' },
      'granny-60': { signature: 175000, prestige: 215000, size: '60 m² (2-Bedroom)', time: '4-5 Months' }
    },
    'custom': {
      'single-mid': { signature: 440000, prestige: 520000, size: '26 Squares (241 m²)', time: '7-9 Months' },
      'single-large': { signature: 520000, prestige: 610000, size: '32 Squares (297 m²)', time: '8-10 Months' },
      'double-mid': { signature: 660000, prestige: 770000, size: '38 Squares (353 m²)', time: '10-12 Months' },
      'double-large': { signature: 820000, prestige: 960000, size: '48 Squares (446 m²)', time: '11-14 Months' },
      'granny-60': { signature: 175000, prestige: 215000, size: '60 m² (2-Bedroom)', time: '4-5 Months' }
    },
    'granny': {
      'granny-60': { signature: 175000, prestige: 215000, size: '60 m² Self Contained', time: '4-5 Months' },
      'single-mid': { signature: 220000, prestige: 260000, size: '80 m² Luxury Studio', time: '5-6 Months' }
    },
    'dual': {
      'double-mid': { signature: 980000, prestige: 1150000, size: '2 x 28 Sq Townhomes', time: '12-14 Months' },
      'double-large': { signature: 1250000, prestige: 1450000, size: '2 x 35 Sq Luxury Units', time: '14-16 Months' }
    }
  };

  const demoCost = 28000;
  const landscapingCost = 35000;

  // DOM Elements
  const typeOptions = calcContainer.querySelectorAll('[data-calc-group="type"] .calc-option');
  const sizeOptions = calcContainer.querySelectorAll('[data-calc-group="size"] .calc-option');
  const tierOptions = calcContainer.querySelectorAll('[data-calc-group="tier"] .calc-option');
  
  const displayAmount = document.getElementById('calcEstimatedTotal');
  const displaySize = document.getElementById('calcHomeSize');
  const displayTime = document.getElementById('calcTimeline');
  const displayDemoRow = document.getElementById('calcDemoRow');
  const displayLandscapeRow = document.getElementById('calcLandscapeRow');
  const displayBaseCost = document.getElementById('calcBaseCost');

  function calculate() {
    let typeData = basePrices[state.projectType] || basePrices['kdr'];
    let planData = typeData[state.sizeConfig] || Object.values(typeData)[0];
    
    let base = planData[state.finishTier] || planData['signature'];
    let total = base;

    // Additional options
    if (state.projectType === 'kdr' && state.includeDemo) {
      total += demoCost;
      if (displayDemoRow) displayDemoRow.style.display = 'flex';
    } else {
      if (displayDemoRow) displayDemoRow.style.display = 'none';
    }

    if (state.includeLandscaping) {
      total += landscapingCost;
      if (displayLandscapeRow) displayLandscapeRow.style.display = 'flex';
    } else {
      if (displayLandscapeRow) displayLandscapeRow.style.display = 'none';
    }

    // Format currency (AUD)
    const formattedTotal = new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      maximumFractionDigits: 0
    }).format(total);

    const formattedBase = new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      maximumFractionDigits: 0
    }).format(base);

    if (displayAmount) displayAmount.textContent = formattedTotal;
    if (displayBaseCost) displayBaseCost.textContent = formattedBase;
    if (displaySize) displaySize.textContent = planData.size;
    if (displayTime) displayTime.textContent = planData.time;
  }

  // Bind clicks
  typeOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      typeOptions.forEach(o => o.classList.remove('active'));
      opt.classList.add('active');
      state.projectType = opt.dataset.val;
      calculate();
    });
  });

  sizeOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      sizeOptions.forEach(o => o.classList.remove('active'));
      opt.classList.add('active');
      state.sizeConfig = opt.dataset.val;
      calculate();
    });
  });

  tierOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      tierOptions.forEach(o => o.classList.remove('active'));
      opt.classList.add('active');
      state.finishTier = opt.dataset.val;
      calculate();
    });
  });

  // Checkbox inputs
  const demoCheck = document.getElementById('calcCheckDemo');
  if (demoCheck) {
    demoCheck.addEventListener('change', (e) => {
      state.includeDemo = e.target.checked;
      calculate();
    });
  }

  const landscapeCheck = document.getElementById('calcCheckLandscape');
  if (landscapeCheck) {
    landscapeCheck.addEventListener('change', (e) => {
      state.includeLandscaping = e.target.checked;
      calculate();
    });
  }

  // Initial run
  calculate();
}

/* ==========================================================================
   3. PORTFOLIO & HOME DESIGNS FILTER
   ========================================================================== */
function initDesignFilters() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const designCards = document.querySelectorAll('.design-card');

  if (!filterBtns.length || !designCards.length) return;

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.dataset.filter;

      designCards.forEach(card => {
        const category = card.dataset.category;
        if (filter === 'all' || category === filter) {
          card.style.display = 'flex';
          card.style.opacity = '0';
          setTimeout(() => {
            card.style.opacity = '1';
          }, 50);
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* ==========================================================================
   4. MODALS & POPUPS
   ========================================================================== */
function initModals() {
  const modalTriggers = document.querySelectorAll('[data-open-modal]');
  const modalOverlays = document.querySelectorAll('.modal-overlay');
  const closeBtns = document.querySelectorAll('.modal-close-btn');

  modalTriggers.forEach(trigger => {
    trigger.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = trigger.dataset.openModal;
      const targetModal = document.getElementById(targetId);
      if (targetModal) {
        targetModal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  closeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      modalOverlays.forEach(m => m.classList.remove('active'));
      document.body.style.overflow = '';
    });
  });

  modalOverlays.forEach(overlay => {
    overlay.addEventListener('click', (e) => {
      if (e.target === overlay) {
        overlay.classList.remove('active');
        document.body.style.overflow = '';
      }
    });
  });

  // Handle floor plan preview modal with room inspection
  window.openPlanDetails = function(name, beds, baths, cars, sq, suburb, imgUrl) {
    const modal = document.getElementById('planModal');
    if (!modal) return;

    activeBlueprintUrl = imgUrl;

    document.getElementById('planModalTitle').textContent = name;
    document.getElementById('planModalSuburb').textContent = suburb;
    document.getElementById('planModalBeds').textContent = beds;
    document.getElementById('planModalBaths').textContent = baths;
    document.getElementById('planModalCars').textContent = cars;
    document.getElementById('planModalSq').textContent = sq;
    
    const imgEl = document.getElementById('planModalImg');
    if (imgEl) {
      imgEl.src = imgUrl;
      imgEl.style.objectFit = 'contain';
      imgEl.style.opacity = '1';
    }

    // Reset room tabs to blueprint
    const tabs = document.querySelectorAll('#planRoomTabs .room-tab-btn');
    tabs.forEach(t => {
      if (t.dataset.roomType === 'blueprint') t.classList.add('active');
      else t.classList.remove('active');
    });

    const listEl = document.getElementById('planModalInclusionsList');
    if (listEl) {
      listEl.innerHTML = defaultPlanInclusions.map(inc => `<li>${inc}</li>`).join('');
    }

    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
  };
}

/* ==========================================================================
   VIP CONCIERGE & WHATSAPP FLOATING HUB
   ========================================================================== */
function initVIPConcierge() {
  const trigger = document.getElementById('vipConciergeTrigger');
  const modal = document.getElementById('vipConciergeModal');
  const closeBtn = document.getElementById('vipCloseBtn');
  if (!trigger || !modal) return;

  trigger.addEventListener('click', (e) => {
    e.stopPropagation();
    modal.classList.toggle('active');
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      modal.classList.remove('active');
    });
  }

  document.addEventListener('click', (e) => {
    if (!modal.contains(e.target) && !trigger.contains(e.target)) {
      modal.classList.remove('active');
    }
  });
}

/* ==========================================================================
   INTERACTIVE FLOOR PLAN ROOM INSPECTOR
   ========================================================================== */
let activeBlueprintUrl = 'assets/images/WhatsApp-Image-2026-09-03-at-3.51.27-PM.jpeg';

const roomPhotos = {
  blueprint: null,
  kitchen: {
    img: 'assets/images/Gemini_Generated_Image_zc6bxgzc6bxgzc6b.jpeg',
    inclusions: [
      '40mm Caesarstone kitchen island with dual waterfall bookmatched gables.',
      'Concealed Butler\'s Pantry with secondary sink and dishwasher recess.',
      '900mm European black glass induction cooktop & twin pyrolytic ovens.',
      'Soft-close Blum push-catch cabinetry with recessed LED linear strip lighting.',
      'Undermount double Franke granite composite sink with pull-out mixer.'
    ]
  },
  master: {
    img: 'assets/images/WhatsApp-Image-2026-09-02-at-10.36.14-PM.jpeg',
    inclusions: [
      'Expansive master retreat zone with private acoustic sound isolation.',
      'Bespoke walk-in dressing wardrobe with floor-to-ceiling timber organizers.',
      'Double glazed architectural picture window with automated blind pelmet.',
      '100% Australian pure wool plush underlay carpeting throughout.',
      'Integrated recessed LED bedside reading wall niches.'
    ]
  },
  ensuite: {
    img: 'assets/images/WhatsApp-Image-2026-09-02-at-10.36.14-PM-1.jpeg',
    inclusions: [
      'Hotel-calibre freestanding composite stone bath with floor-mounted gooseneck tapware.',
      'Full height 600x1200mm rectified porcelain wall and floor tiles.',
      'Walk-in frameless glass shower enclosure with dual rainfall ceiling heads.',
      'Custom floating double vanity with Caesarstone benchtop & backlit LED mirror.',
      'In-wall concealed cistern toilet with matte black actuator plate.'
    ]
  }
};

const defaultPlanInclusions = [
  '2740mm ceiling heights on ground floor with square-set cornices.',
  '40mm Caesarstone kitchen island with dual waterfall gables & butler\'s pantry.',
  'Refrigerated multi-zone inverter cooling & ducted heating.',
  'Floor-to-ceiling porcelain tiles in ensuite and main bathrooms with frameless glass.',
  'Victorian 7-Star NatHERS double glazed energy compliance throughout.'
];

function initRoomInspector() {
  const tabsContainer = document.getElementById('planRoomTabs');
  const imgEl = document.getElementById('planModalImg');
  const listEl = document.getElementById('planModalInclusionsList');
  if (!tabsContainer || !imgEl) return;

  const buttons = tabsContainer.querySelectorAll('.room-tab-btn');
  buttons.forEach(btn => {
    btn.addEventListener('click', () => {
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const room = btn.dataset.roomType;
      imgEl.style.opacity = '0.3';
      imgEl.style.transform = 'scale(0.98)';
      imgEl.style.transition = 'all 0.25s ease';

      setTimeout(() => {
        if (room === 'blueprint') {
          imgEl.src = activeBlueprintUrl;
          imgEl.style.objectFit = 'contain';
          if (listEl) {
            listEl.innerHTML = defaultPlanInclusions.map(inc => `<li>${inc}</li>`).join('');
          }
        } else {
          const roomData = roomPhotos[room];
          if (roomData) {
            imgEl.src = roomData.img;
            imgEl.style.objectFit = 'cover';
            if (listEl) {
              listEl.innerHTML = roomData.inclusions.map(inc => `<li>${inc}</li>`).join('');
            }
          }
        }
        imgEl.style.opacity = '1';
        imgEl.style.transform = 'scale(1)';
      }, 150);
    });
  });
}

/* ==========================================================================
   5. FAQ ACCORDION
   ========================================================================== */
function initFAQ() {
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    const question = item.querySelector('.faq-question');
    if (!question) return;

    question.addEventListener('click', () => {
      const isOpen = item.classList.contains('active');
      faqItems.forEach(i => i.classList.remove('active'));
      if (!isOpen) {
        item.classList.add('active');
      }
    });
  });
}

/* ==========================================================================
   6. CONSULTATION & ESTIMATE INQUIRY FORM
   ========================================================================== */
function initConsultationForm() {
  const form = document.getElementById('consultationForm');
  if (!form) return;

  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;

    btn.innerHTML = `
      <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-linecap="round"></circle>
      </svg>
      Processing Feasibility...
    `;
    btn.disabled = true;

    setTimeout(() => {
      form.innerHTML = `
        <div style="text-align: center; padding: 2rem 1rem;">
          <div style="width: 64px; height: 64px; background: rgba(34, 197, 94, 0.15); color: #22C55E; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto;">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12"></polyline>
            </svg>
          </div>
          <h3 style="font-size: 1.5rem; margin-bottom: 0.5rem; color: #0F172A;">Site Feasibility Request Received!</h3>
          <p style="color: #64748B; font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.6;">
            Thank you. Senior Builder Director at Intellect Homes will review your property address, zoning, and orientation. We will call you within 24 business hours to deliver your preliminary feasibility summary.
          </p>
          <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 1rem; font-size: 0.85rem; color: #334155;">
            <strong>Immediate Urgent Inquiries:</strong> Call directly at <a href="tel:+61411560177" style="color: #D4AF37; font-weight: 700;">+61 411 560 177</a>
          </div>
        </div>
      `;
    }, 1200);
  });
}

/* ==========================================================================
   7. SCROLL-REVEAL ENHANCEMENTS
   ========================================================================== */
function initScrollAnimations() {
  const cards = document.querySelectorAll('.service-card, .design-card, .timeline-card, .testimonial-card');
  if (!('IntersectionObserver' in window)) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(24px)';
    card.style.transition = 'opacity 0.6s cubic-bezier(0.16, 1, 0.3, 1), transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
    observer.observe(card);
  });
}

// Call scroll reveal
document.addEventListener('DOMContentLoaded', () => {
  initScrollAnimations();
  initBeforeAfterSlider();
  initSpotlightCards();
  initStatCounters();
});

/* ==========================================================================
   8. 2026 TREND: BEFORE & AFTER INTERACTIVE SLIDER
   ========================================================================== */
function initBeforeAfterSlider() {
  const wrappers = document.querySelectorAll('.before-after-wrapper');
  wrappers.forEach(wrapper => {
    const afterImg = wrapper.querySelector('.before-after-img.after');
    const handle = wrapper.querySelector('.before-after-handle');
    if (!afterImg || !handle) return;

    let isDown = false;

    function move(clientX) {
      const rect = wrapper.getBoundingClientRect();
      let x = clientX - rect.left;
      if (x < 30) x = 30;
      if (x > rect.width - 30) x = rect.width - 30;

      const percentage = (x / rect.width) * 100;
      afterImg.style.width = percentage + '%';
      handle.style.left = percentage + '%';
    }

    wrapper.addEventListener('mousedown', (e) => {
      isDown = true;
      move(e.clientX);
    });

    window.addEventListener('mouseup', () => {
      isDown = false;
    });

    window.addEventListener('mousemove', (e) => {
      if (!isDown) return;
      move(e.clientX);
    });

    // Touch support for iPad / Mobile
    wrapper.addEventListener('touchstart', (e) => {
      isDown = true;
      move(e.touches[0].clientX);
    }, { passive: true });

    window.addEventListener('touchend', () => {
      isDown = false;
    });

    window.addEventListener('touchmove', (e) => {
      if (!isDown) return;
      move(e.touches[0].clientX);
    }, { passive: true });
  });
}

/* ==========================================================================
   9. 2026 TREND: SPOTLIGHT CURSOR MOUSE-TRACKING GLOW
   ========================================================================== */
function initSpotlightCards() {
  const cards = document.querySelectorAll('.spotlight-card, .service-card, .design-card');
  cards.forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      card.style.setProperty('--mouse-x', `${x}px`);
      card.style.setProperty('--mouse-y', `${y}px`);
    });
  });
}

/* ==========================================================================
   10. 2026 TREND: DYNAMIC STAT COUNTER ANIMATION (KINETIC EASE-OUT)
   ========================================================================== */
function initStatCounters() {
  const statNumbers = document.querySelectorAll('.stat-number');
  if (!statNumbers.length) return;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const originalText = el.textContent.trim();
        const match = originalText.match(/^(\D*)(\d+)(\D*)$/);
        
        if (match && parseInt(match[2], 10) > 0) {
          const prefix = match[1] || '';
          const targetNum = parseInt(match[2], 10);
          const suffix = match[3] || '';
          
          let startTime = null;
          const duration = 1400; // 1.4s smooth luxury duration

          function step(timestamp) {
            if (!startTime) startTime = timestamp;
            const progress = Math.min((timestamp - startTime) / duration, 1);
            // Ease-out cubic curve
            const ease = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(ease * targetNum);
            el.textContent = `${prefix}${current}${suffix}`;
            
            if (progress < 1) {
              requestAnimationFrame(step);
            } else {
              el.textContent = originalText;
            }
          }
          requestAnimationFrame(step);
        }

        el.style.transition = 'transform 0.6s cubic-bezier(0.16, 1, 0.3, 1)';
        el.style.transform = 'scale(1.08)';
        setTimeout(() => {
          el.style.transform = 'scale(1)';
        }, 250);

        observer.unobserve(el);
      }
    });
  }, { threshold: 0.4 });

  statNumbers.forEach(stat => observer.observe(stat));
}
