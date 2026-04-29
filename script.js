const sample = (items) => items[Math.floor(Math.random() * items.length)];

const samples = {
  firstNames: [
    "Amelia",
    "Noah",
    "Isabella",
    "Theo",
    "Charlotte",
    "Julian",
    "Maya",
    "Elias",
    "Violet",
    "Rowan",
    "Sofia",
    "Lucas"
  ],
  lastNames: [
    "Bennett",
    "Holloway",
    "Monroe",
    "Ellis",
    "Hart",
    "Sullivan",
    "Reed",
    "Kensington",
    "Flores",
    "Whitaker"
  ],
  cities: [
    { city: "Charleston", state: "South Carolina", airport: "Charleston International Airport (CHS)" },
    { city: "Napa", state: "California", airport: "San Francisco International Airport (SFO)" },
    { city: "Savannah", state: "Georgia", airport: "Savannah/Hilton Head International Airport (SAV)" },
    { city: "Asheville", state: "North Carolina", airport: "Asheville Regional Airport (AVL)" },
    { city: "Newport", state: "Rhode Island", airport: "T. F. Green Airport (PVD)" }
  ],
  venues: [
    "The Glass Conservatory",
    "Harborview House",
    "Oak & Ivy Estate",
    "Moonlit Garden Pavilion",
    "Seabrook Manor",
    "The Willow Atrium"
  ],
  ceremonySites: [
    "Rose Garden Lawn",
    "Sunset Terrace",
    "Magnolia Courtyard",
    "Cliffside Arbor",
    "North Orchard Pergola"
  ],
  receptionSites: [
    "Grand Ballroom",
    "Lakeside Marquee",
    "Candlelight Hall",
    "Atrium Dining Room",
    "Vineyard Reception Tent"
  ],
  planners: [
    "Juniper Lane Events",
    "Ever After Collective",
    "North Star Weddings",
    "Velvet Table Planning",
    "Heirloom Celebration Co."
  ],
  florists: [
    "Golden Hour Florals",
    "Petal Theory",
    "Wild Bloom Studio",
    "Blue Iris Floral Design",
    "Meadow & Stem"
  ],
  photographers: [
    "Olive & Film Studio",
    "Fable Light Photography",
    "Maple Street Portraits",
    "North Harbor Photo",
    "Junebug Image Co."
  ],
  bands: [
    "The Lantern District",
    "Velvet City Orchestra",
    "The Daydream Classics",
    "Midnight Carousel",
    "The Golden Tones"
  ],
  signatureDrinks: [
    "Lavender French 75",
    "Rosemary Paloma",
    "Blackberry Bourbon Smash",
    "Blood Orange Spritz",
    "Pear Elderflower Collins"
  ],
  cuisines: [
    "coastal American",
    "modern Italian",
    "seasonal farm-to-table",
    "Mediterranean-inspired",
    "Southern comfort"
  ],
  desserts: [
    "brown butter cake with vanilla bean frosting",
    "lemon olive oil cake with berry compote",
    "champagne cake with raspberry filling",
    "almond cake with honey mascarpone",
    "chocolate hazelnut cake with espresso cream"
  ],
  colors: [
    "sage green, ivory, and champagne",
    "dusty blue, cream, and gold",
    "terracotta, blush, and soft peach",
    "forest green, taupe, and candlelight white",
    "lavender, pearl, and warm gray"
  ],
  transportTypes: [
    "continuous coach shuttles",
    "vintage trolley service",
    "black car transfers",
    "sprinter van loops",
    "water taxi pickups"
  ],
  postEvents: [
    "farewell brunch",
    "group beach walk",
    "winery tasting",
    "coffee bar send-off",
    "garden picnic"
  ],
  welcomeEvents: [
    "welcome cocktails",
    "sunset rehearsal dinner",
    "family pizza night",
    "rooftop meet-and-greet",
    "dessert and jazz social"
  ],
  interests: [
    "hosting elaborate dinner parties",
    "hiking coastal trails",
    "collecting cookbooks from every trip",
    "spending Sundays at the farmers market",
    "turning every holiday into a themed gathering"
  ],
  proposalMoments: [
    "during a golden-hour sail",
    "beneath a canopy of string lights in their backyard",
    "while visiting the city where they first met",
    "on a snowy mountain overlook",
    "at the end of a private picnic in the vineyard"
  ],
  weatherBackups: [
    "If rain arrives, the ceremony moves inside the glass atrium without changing the schedule.",
    "Umbrellas and patio heaters will be available if the evening turns cool.",
    "Shuttle dispatch texts will be sent if weather causes traffic delays.",
    "Indoor cocktail spaces are reserved if winds become too strong for the lawn."
  ],
  faqQuestions: [
    "Can I bring my children?",
    "Will the ceremony and reception be outdoors?",
    "What time should I arrive?",
    "Is there parking on site?",
    "Can dietary restrictions be accommodated?",
    "What should I wear for the welcome event?",
    "Will there be transportation after the reception?",
    "Are phones allowed during the ceremony?"
  ]
};

const chooseUniquePair = () => {
  const first = sample(samples.firstNames);
  let second = sample(samples.firstNames);
  while (second === first) {
    second = sample(samples.firstNames);
  }

  return [
    `${first} ${sample(samples.lastNames)}`,
    `${second} ${sample(samples.lastNames)}`
  ];
};

const formatDate = (date) =>
  date.toLocaleDateString("en-US", {
    weekday: "long",
    month: "long",
    day: "numeric",
    year: "numeric"
  });

const formatTime = (date) =>
  date.toLocaleTimeString("en-US", {
    hour: "numeric",
    minute: "2-digit"
  });

const createFutureDate = () => {
  const date = new Date();
  date.setDate(date.getDate() + Math.floor(Math.random() * 250) + 45);
  date.setHours(16 + Math.floor(Math.random() * 2), 0, 0, 0);
  return date;
};

const weddingDate = createFutureDate();
const city = sample(samples.cities);
const [partnerOne, partnerTwo] = chooseUniquePair();
const venue = sample(samples.venues);
const ceremonySite = sample(samples.ceremonySites);
const receptionSite = sample(samples.receptionSites);
const welcomeEvent = sample(samples.welcomeEvents);
const afterEvent = sample(samples.postEvents);
const signatureDrinkOne = sample(samples.signatureDrinks);
let signatureDrinkTwo = sample(samples.signatureDrinks);
while (signatureDrinkTwo === signatureDrinkOne) {
  signatureDrinkTwo = sample(samples.signatureDrinks);
}

const travelLeadDays = 2 + Math.floor(Math.random() * 2);
const rsvpDate = new Date(weddingDate);
rsvpDate.setDate(rsvpDate.getDate() - 42);

const schedule = [
  {
    label: "Thursday",
    title: welcomeEvent[0].toUpperCase() + welcomeEvent.slice(1),
    time: "6:00 PM - 8:30 PM",
    description: `Guests are invited to informal ${welcomeEvent} at ${venue}'s terrace bar. Smart casual attire encouraged.`
  },
  {
    label: "Friday",
    title: "Guest arrival & check-in",
    time: "2:00 PM onward",
    description: `Hotel block check-in opens, with hospitality bags available in the lobby and local recommendations at the welcome desk.`
  },
  {
    label: "Saturday",
    title: "Ceremony",
    time: `${formatTime(weddingDate)} at ${ceremonySite}`,
    description: `Ceremony doors open 30 minutes early. Guests are asked to be seated 15 minutes before the processional begins.`
  },
  {
    label: "Saturday",
    title: "Cocktail hour & reception",
    time: "Immediately following ceremony",
    description: `Cocktail hour begins on the lawn, followed by dinner, speeches, dancing, and a late-night snack inside the ${receptionSite}.`
  },
  {
    label: "Sunday",
    title: afterEvent[0].toUpperCase() + afterEvent.slice(1),
    time: "10:30 AM - 12:30 PM",
    description: `A relaxed ${afterEvent} gives everyone time for one final visit before departures.`
  }
];

const weddingParty = [
  { role: "Maid of Honor", person: `${sample(samples.firstNames)} ${sample(samples.lastNames)}` },
  { role: "Best Man", person: `${sample(samples.firstNames)} ${sample(samples.lastNames)}` },
  { role: "Bridesmaid", person: `${sample(samples.firstNames)} ${sample(samples.lastNames)}` },
  { role: "Bridesmaid", person: `${sample(samples.firstNames)} ${sample(samples.lastNames)}` },
  { role: "Groomsman", person: `${sample(samples.firstNames)} ${sample(samples.lastNames)}` },
  { role: "Groomsman", person: `${sample(samples.firstNames)} ${sample(samples.lastNames)}` }
];

const faqAnswers = {
  "Can I bring my children?": "This example wedding is adults-only for the ceremony and reception, with infants in arms welcome.",
  "Will the ceremony and reception be outdoors?": `The ceremony is outdoors at ${ceremonySite}, and the reception moves into the ${receptionSite}.`,
  "What time should I arrive?": "Please arrive 30 minutes before the ceremony so there is enough time for seating.",
  "Is there parking on site?": "Yes. Complimentary valet and self-parking are both available at the venue.",
  "Can dietary restrictions be accommodated?": "Yes. Guests can note allergies or dietary needs on the RSVP form, and the caterer will prepare labeled meals.",
  "What should I wear for the welcome event?": "The welcome event is smart casual; think dresses, slacks, polished separates, and light layers.",
  "Will there be transportation after the reception?": "Yes. Return shuttles loop between the venue and host hotels every 20 minutes until the final sendoff.",
  "Are phones allowed during the ceremony?": "Guests are invited to enjoy an unplugged ceremony and take photos once cocktail hour begins."
};

const details = {
  summary: `${partnerOne} and ${partnerTwo} invite you to a full wedding weekend in ${city.city}, ${city.state}, with every key detail included for guests.`,
  story: `${partnerOne} and ${partnerTwo} built their relationship around ${sample(samples.interests)}. After years of traveling together, introducing each other to favorite traditions, and planning parties for friends, they decided to host a wedding that feels warm, organized, and joyfully detailed from start to finish.`,
  overview: [
    { label: "Weekend destination", value: `${city.city}, ${city.state}` },
    { label: "Main venue", value: `${venue}, ${city.city}` },
    { label: "RSVP deadline", value: formatDate(rsvpDate) },
    { label: "Dress code", value: "Formal garden party" }
  ],
  quickNotes: [
    "Ceremony begins promptly; arrive at least 30 minutes early.",
    "Most events are within a 15-minute radius of the hotel block.",
    "An unplugged ceremony will be followed by an open-photo reception.",
    `Color palette for the weekend: ${sample(samples.colors)}.`
  ],
  proposalDetails: [
    `Proposal moment: ${partnerOne.split(" ")[0]} proposed to ${partnerTwo.split(" ")[0]} ${sample(samples.proposalMoments)}.`,
    `Planner: ${sample(samples.planners)} is coordinating the full weekend experience.`,
    `Photographer: ${sample(samples.photographers)} will document the day.`,
    `Florals: ${sample(samples.florists)} will design the ceremony and reception arrangements.`
  ],
  ceremonyDetails: [
    `Venue address: ${venue}, 214 Celebration Lane, ${city.city}, ${city.state}.`,
    `Ceremony location: ${ceremonySite}.`,
    `Start time: ${formatTime(weddingDate)} with seating beginning 30 minutes before.`,
    "Length: approximately 30 minutes.",
    "Ceremony style: unplugged and officiated by a close friend of the couple.",
    sample(samples.weatherBackups)
  ],
  receptionDetails: [
    `Reception space: ${receptionSite}.`,
    "Cocktail hour starts immediately after the ceremony with passed appetizers and live music.",
    `Dinner service features ${sample(samples.cuisines)} cuisine with table-side wine service.`,
    `Signature drinks: ${signatureDrinkOne} and ${signatureDrinkTwo}.`,
    `Live entertainment: ${sample(samples.bands)}.`,
    "The evening concludes with a sparkler exit and late-night snack station."
  ],
  familyDetails: [
    `Hosts: Together with their families, ${partnerOne} and ${partnerTwo} are delighted to celebrate with you.`,
    `Ceremony readers include siblings and lifelong friends from both sides.`,
    "Grandparents and family elders will be seated before general guest seating begins.",
    "A private family photo session is scheduled immediately after the ceremony."
  ],
  lodgingDetails: [
    `Primary hotel block: The Marlowe House, 0.8 miles from ${venue}.`,
    "Secondary hotel block: The Bellview Suites, featuring discounted weekend rates through the RSVP deadline.",
    "Hospitality bags will be available at both host hotels beginning Friday afternoon.",
    "Early booking is recommended because the city is hosting a seasonal food festival that same weekend."
  ],
  transportDetails: [
    `Transportation plan: ${sample(samples.transportTypes)} between hotel blocks, welcome event, ceremony, and reception.`,
    "Valet parking is available for guests who prefer to drive.",
    "Accessible transportation can be arranged in advance through the wedding planner.",
    "The final shuttle departs 30 minutes after the last dance."
  ],
  arrivalDetails: [
    `Recommended airport: ${city.airport}.`,
    `Suggested arrival: ${travelLeadDays} days before the wedding for guests attending all weekend events.`,
    "Ride-share pickup is reliable from the airport, and the hotel concierge can coordinate private transfers.",
    "Out-of-town guests should reserve lodging before booking rental cars, since most wedding transportation is included."
  ],
  attireDetails: [
    "Ceremony and reception attire: formal garden party.",
    "Women may prefer block heels or wedges for lawn pathways.",
    "Men are encouraged to wear dark suits or tuxedos.",
    "A shawl or jacket is recommended for the evening if temperatures cool after sunset."
  ],
  menuDetails: [
    `Dinner style: plated ${sample(samples.cuisines)} menu.`,
    "Sample first course: heirloom tomato salad with whipped ricotta and basil oil.",
    "Entree options: filet with roasted vegetables, herb salmon, or wild mushroom risotto.",
    `Dessert: ${sample(samples.desserts)} plus a miniature pastry table.`,
    "Late-night bite: truffle fries, sliders, and espresso service."
  ],
  guestDetails: [
    "Check-in signage will direct guests to seating, restrooms, and the gift table.",
    "A quiet lounge will be available during the reception for anyone needing a low-volume space.",
    "Ceremony programs include a QR code linking to the full itinerary and shuttle loop.",
    "Guest book, custom favors, and photo booth open after dinner service begins."
  ],
  preEvents: [
    {
      title: "Thursday evening welcome",
      body: `An easygoing ${welcomeEvent} with local bites, wine, and acoustic music gives early arrivals time to settle in and meet other guests.`
    },
    {
      title: "Friday rehearsal gathering",
      body: "Wedding party members and immediate family will receive a separate invitation with rehearsal timing, transportation, and lineup instructions."
    }
  ],
  postEvents: [
    {
      title: "Sunday sendoff",
      body: `The ${afterEvent} is open to all guests staying through Sunday and includes coffee, brunch favorites, and a final toast.`
    },
    {
      title: "Departure support",
      body: "The planning team will share airport departure windows and recommended shuttle sign-up times at check-in."
    }
  ],
  faq: samples.faqQuestions.map((question) => ({
    question,
    answer: faqAnswers[question]
  })),
  registryDetails: [
    "The couple is registered for homewares, luggage, and experience gifts.",
    "A contribution fund is available for their future honeymoon and first-home garden project.",
    "Your presence is the most meaningful gift, and all gifting options are completely optional."
  ],
  contactDetails: [
    `Primary wedding contact: ${sample(samples.planners)}, weekend coordination team.`,
    "Emergency day-of phone: (555) 014-2987.",
    "Guest RSVP support email: celebrate@weddingweekend.example.",
    sample(samples.weatherBackups)
  ]
};

const setText = (id, value) => {
  const element = document.getElementById(id);
  if (element) {
    element.textContent = value;
  }
};

const renderList = (id, items) => {
  const element = document.getElementById(id);
  if (!element) {
    return;
  }

  element.innerHTML = items.map((item) => `<li>${item}</li>`).join("");
};

const renderOverviewCards = () => {
  const container = document.getElementById("overview-cards");
  container.innerHTML = details.overview
    .map(
      (item) => `
        <div class="stat">
          <span class="stat__label">${item.label}</span>
          <strong>${item.value}</strong>
        </div>
      `
    )
    .join("");
};

const renderSchedule = () => {
  const container = document.getElementById("schedule-grid");
  container.innerHTML = schedule
    .map(
      (event) => `
        <article class="card timeline-card">
          <p class="timeline-card__label">${event.label}</p>
          <h3>${event.title}</h3>
          <strong>${event.time}</strong>
          <p>${event.description}</p>
        </article>
      `
    )
    .join("");
};

const renderParty = () => {
  const container = document.getElementById("wedding-party");
  container.innerHTML = weddingParty
    .map(
      (member) => `
        <div class="party-card">
          <span>${member.role}</span>
          <strong>${member.person}</strong>
        </div>
      `
    )
    .join("");
};

const renderEventStack = (id, items) => {
  const container = document.getElementById(id);
  container.innerHTML = items
    .map(
      (item) => `
        <div class="stack-card">
          <h4>${item.title}</h4>
          <p>${item.body}</p>
        </div>
      `
    )
    .join("");
};

const renderFaq = () => {
  const container = document.getElementById("faq-list");
  container.innerHTML = details.faq
    .map(
      (item) => `
        <article class="card faq-card">
          <h3>${item.question}</h3>
          <p>${item.answer}</p>
        </article>
      `
    )
    .join("");
};

const renderCountdown = () => {
  const today = new Date();
  const msPerDay = 1000 * 60 * 60 * 24;
  const days = Math.max(0, Math.ceil((weddingDate - today) / msPerDay));
  setText("countdown", `${days} days to go`);
};

setText("couple-names", `${partnerOne} & ${partnerTwo}`);
setText("wedding-summary", details.summary);
setText("wedding-date", formatDate(weddingDate));
setText("wedding-location", `${city.city}, ${city.state}`);
setText("couple-story", details.story);

renderCountdown();
renderOverviewCards();
renderList("quick-notes", details.quickNotes);
renderList("proposal-details", details.proposalDetails);
renderSchedule();
renderList("ceremony-details", details.ceremonyDetails);
renderList("reception-details", details.receptionDetails);
renderParty();
renderList("family-details", details.familyDetails);
renderList("lodging-details", details.lodgingDetails);
renderList("transport-details", details.transportDetails);
renderList("arrival-details", details.arrivalDetails);
renderList("attire-details", details.attireDetails);
renderList("menu-details", details.menuDetails);
renderList("guest-details", details.guestDetails);
renderEventStack("pre-events", details.preEvents);
renderEventStack("post-events", details.postEvents);
renderFaq();
renderList("registry-details", details.registryDetails);
renderList("contact-details", details.contactDetails);
