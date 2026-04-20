const { createApp } = Vue;
const API_BASE = window.location.origin;

createApp({

  /* ── DATA ── */
  data() {
    return {
      // UI state
      navScrolled:    false,
      menuOpen:       false,
      activeSection:  'home',
      formSubmitting: false,
      formSubmitted:  false,
      apiError:       false,

      form: { name: '', email: '', projectType: '', message: '' },

      // ── All content fetched from backend
      projects:     [],
      services:     [],
      skillGroups:  [],
      chips:        [],   // array of strings
      values:       [],   // [{ num, title, desc }]
      contactItems: [],   // [{ id, abbr, label, href, display, external }]

      // ── Ticker (static, not editable)
      tickerItems: [
        'LLM Agents', 'Workflow Automation', 'Multi-Agent Systems',
        'RAG Pipelines', 'AI APIs', 'FastAPI Backends',
        'Voice Assistants', 'Process Automation', 'LangChain', 'Prompt Engineering',
      ],

      // ── Contact form select options (static)
      projectTypeOptions: [
        { value: 'agent',      label: 'Agentic AI System' },
        { value: 'automation', label: 'Workflow Automation' },
        { value: 'rag',        label: 'RAG / Knowledge System' },
        { value: 'backend',    label: 'AI Backend API' },
        { value: 'voice',      label: 'Voice AI Assistant' },
        { value: 'consult',    label: 'Consulting / Strategy' },
        { value: 'other',      label: 'Other' },
      ],
    };
  },

  /* ── METHODS ── */
  methods: {

    // ── Fetch all site data from API ─────────────────────────────────────────
    async fetchSiteData() {
      try {
        const res  = await fetch(`${API_BASE}/api/site-data`);
        if (!res.ok) throw new Error('API error');
        const data = await res.json();

        // Projects — direct mapping (backend matches frontend shape)
        this.projects = data.projects;

        // Services — backend uses `list_items`, template uses `list`
        this.services = data.services.map(s => ({
          ...s,
          list: s.list_items,
        }));

        // Skills — direct mapping
        this.skillGroups = data.skillGroups;

        // Chips — array of {id, name, sort_order} → array of strings
        this.chips = data.chips.map(c => c.name);

        // Values — backend uses `description`, template uses `desc`
        this.values = data.values.map(v => ({
          num:  v.num,
          title: v.title,
          desc: v.description,
        }));

        // Contact items — backend uses `is_external`, template uses `external`
        this.contactItems = data.contactItems.map(c => ({
          id:       c.id,
          abbr:     c.abbr,
          label:    c.label,
          href:     c.href,
          display:  c.display,
          external: c.is_external,
        }));

      } catch (err) {
        console.error('Could not reach API:', err);
        this.apiError = true;

        this.projects = [
          {
            id: 1,
            title: "AI Assistant RAG",
            desc: "Retrieval-based assistant using vector DB",
            tags: ["RAG", "LLM"],
            stack: ["Python", "LangChain"],
            link: "#"
          }
        ];

        this.services = [
          {
            id: 1,
            title: "Agentic AI Systems",
            desc: "Build intelligent multi-agent systems",
            list: ["LangChain", "Multi-agent", "Automation"]
          }
        ];

        this.skillGroups = [
          {
            title: "AI & LLM",
            color: "cyan",
            skills: ["LangChain", "Prompt Engineering"]
          }
        ];

        this.chips = ["AI", "Automation", "LLM"];
        this.values = [
          { num: "01", title: "Results First", desc: "Solve real problems" }
        ];

        this.contactItems = [];
      }
    },

    // ── Contact form submit ──────────────────────────────────────────────────
    async submitForm() {
      if (!this.form.name || !this.form.email || !this.form.message) return;
      this.formSubmitting = true;
      try {
        const payload = {
          name: this.form.name,
          email: this.form.email,
          projectType: this.form.projectType,
          message: this.form.message
        };
        const res = await fetch(`${API_BASE}/api/messages`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Failed to send message');
        
        this.formSubmitted  = true;
        this.form = { name: '', email: '', projectType: '', message: '' };
        
        // Hide success message after 6 seconds
        setTimeout(() => { this.formSubmitted = false; }, 6000);
      } catch (err) {
        console.error('Contact form error:', err);
        alert("There was an issue sending your message. Please email me directly!");
      } finally {
        this.formSubmitting = false;
      }
    },

    // ── Particle canvas ──────────────────────────────────────────────────────
    initParticles() {
      const canvas = document.getElementById('particle-canvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      let particles = [];
      const mouse   = { x: null, y: null };
      let animFrame;

      const resize = () => {
        canvas.width  = window.innerWidth;
        canvas.height = window.innerHeight;
      };
      resize();
      const reinit = () => { resize(); particles = []; init(); animate(); };
      window.addEventListener('resize', reinit);
      window.addEventListener('mousemove', e => { mouse.x = e.clientX; mouse.y = e.clientY; });
      window.addEventListener('mouseleave', () => { mouse.x = null; mouse.y = null; });

      class Particle {
        constructor() { this.reset(); }
        reset() {
          this.x    = Math.random() * canvas.width;
          this.y    = Math.random() * canvas.height;
          this.vx   = (Math.random() - 0.5) * 0.4;
          this.vy   = (Math.random() - 0.5) * 0.4;
          this.r    = Math.random() * 1.5 + 0.5;
          const c   = ['rgba(74,144,217,', 'rgba(108,126,225,', 'rgba(59,130,246,'];
          this.base = c[Math.floor(Math.random() * c.length)];
          this.alpha     = Math.random() * 0.5 + 0.15;
          this.baseAlpha = this.alpha;
        }
        update() {
          this.x += this.vx;
          this.y += this.vy;
          if (this.x < 0 || this.x > canvas.width)  this.vx *= -1;
          if (this.y < 0 || this.y > canvas.height)  this.vy *= -1;
          if (mouse.x !== null) {
            const dx = this.x - mouse.x, dy = this.y - mouse.y;
            const d  = Math.sqrt(dx * dx + dy * dy);
            this.alpha = d < 100 ? Math.min(1, this.baseAlpha + 0.5 * (1 - d / 100)) : this.baseAlpha;
          }
        }
        draw() {
          ctx.beginPath();
          ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
          ctx.fillStyle = this.base + this.alpha + ')';
          ctx.fill();
        }
      }

      const init = () => {
        particles = [];
        const n = Math.min(Math.floor((canvas.width * canvas.height) / 10000), 140);
        for (let i = 0; i < n; i++) particles.push(new Particle());
      };

      const drawLines = () => {
        for (let i = 0; i < particles.length; i++) {
          for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const d  = Math.sqrt(dx * dx + dy * dy);
            if (d < 120) {
              ctx.beginPath();
              ctx.moveTo(particles[i].x, particles[i].y);
              ctx.lineTo(particles[j].x, particles[j].y);
              ctx.strokeStyle = `rgba(74,144,217,${(1 - d / 120) * 0.1})`;
              ctx.lineWidth   = 0.8;
              ctx.stroke();
            }
          }
        }
      };

      const animate = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        particles.forEach(p => { p.update(); p.draw(); });
        drawLines();
        animFrame = requestAnimationFrame(animate);
      };

      this._stopParticles = () => cancelAnimationFrame(animFrame);

      document.addEventListener('visibilitychange', () => {
        if (document.hidden) cancelAnimationFrame(animFrame);
        else animate();
      });

      init();
      animate();
    },

    // ── Scroll-reveal ────────────────────────────────────────────────────────
    initScrollReveal() {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const siblings = [...entry.target.parentElement.querySelectorAll('.reveal')];
            const i        = siblings.indexOf(entry.target);
            entry.target.style.transitionDelay = `${(i % 6) * 80}ms`;
            entry.target.classList.add('visible');
            obs.unobserve(entry.target);
          }
        });
      }, { threshold: 0.12 });
      document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
    },

    // ── Active section highlight ─────────────────────────────────────────────
    initSectionObserver() {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) this.activeSection = entry.target.id;
        });
      }, { rootMargin: '-40% 0px -55% 0px' });
      document.querySelectorAll('section[id]').forEach(s => obs.observe(s));
    },
  },

  /* ── LIFECYCLE ── */
  async mounted() {
    // Fetch live content from backend
    await this.fetchSiteData();

    // Navbar scroll
    window.addEventListener('scroll', () => {
      this.navScrolled = window.scrollY > 40;
    });

    // Particle canvas
    this.initParticles();

    // Wait for Vue to render data-driven DOM before attaching observers
    this.$nextTick(() => {
      this.initScrollReveal();
      this.initSectionObserver();
    });

    console.log('%c Aakash Dandekar', 'color:#4a90d9;font-size:2rem;font-weight:900;');
    console.log('%c Vue 3 + FastAPI · Built by Aakash Dandekar', 'color:#8a96aa;');
  },

  beforeUnmount() {
    if (this._stopParticles) this._stopParticles();
  },

}).mount('#app');
