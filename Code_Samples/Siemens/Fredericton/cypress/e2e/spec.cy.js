describe("Mohammadali Rahnama Resume Page", () => {
  beforeEach(() => {
    // Visit the URL
    cy.visit("https://rahnama.uk/"); // replace with your actual website url
  });

  it("Successfully loads", () => {
    cy.visit("https://rahnama.uk/"); // replace with your actual website url
  });

  it("Should have the correct title", () => {
    cy.title().should("include", "Mohammadali Rahnama Resume");
  });

  it("Should display the name correctly", () => {
    cy.get("h1").contains("Mohammadali Rahnama");
  });

  it("Should display the profession correctly", () => {
    cy.get("h2").contains(
      "Computer Engineer with Strong Testing & Automation Background"
    );
  });

  // Testing the email link
  it("Should have the correct email link", () => {
    cy.get('.contact-info > a[href="mailto:contact@morahnama.com"]');
  });

  // Testing the phone number link
  it("Should have the correct phone number link", () => {
    cy.get('.contact-info > a[href="tel:+15064000402"]');
  });

  // Testing the LinkedIn link
  it("Should have the correct LinkedIn link", () => {
    cy.get(
      '.contact-info > a[href="https://www.linkedin.com/in/mohammadali-rahnama-4170b0a9/"]'
    );
  });

  // Testing the GitHub link
  it("Should have the correct GitHub link", () => {
    cy.get('.contact-info > a[href="https://github.com/morahnama"]');
  });

  // Testing the PDF download link
  it("Should have the correct download link", () => {
    cy.get("#download-btn").should(
      "have.attr",
      "href",
      "MohammadaliRahnamaResume.pdf"
    );
  });

  // Add more tests as per your requirements
});

describe("API Test", () => {
  it("GET - read", () => {
    cy.request(
      "GET",
      "https://my-json-server.typicode.com/MoRahnama/JSONAPI/users"
    ).then((response) => {
      expect(response).to.have.property("status", 200);
      expect(response.body).to.not.be.null;
      expect(response.body).to.have.length(10);

      response.body.forEach((user) => {
        expect(user).to.have.all.keys(
          "id",
          "name",
          "username",
          "email",
          "address",
          "phone",
          "website",
          "company"
        );
      });
    });
  });

  it("PUT - update", () => {
    cy.request({
      method: "PUT",
      url: "https://my-json-server.typicode.com/MoRahnama/JSONAPI/users/1",
      body: {
        id: 1,
        name: "Updated name",
        username: "Updated username",
        email: "Updated email",
        address: "Updated address",
        phone: "Updated phone",
        website: "Updated website",
        company: "Updated company",
      },
    }).then((response) => {
      expect(response).to.have.property("status", 200);
      expect(response.body).to.not.be.null;
      expect(response.body).to.have.all.keys(
        "id",
        "name",
        "username",
        "email",
        "address",
        "phone",
        "website",
        "company"
      );
      expect(response.body).to.include({
        name: "Updated name",
        username: "Updated username",
      });
    });
  });
});
