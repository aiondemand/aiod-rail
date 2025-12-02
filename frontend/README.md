# AiodRailFrontend

This project was generated using [Angular CLI](https://github.com/angular/angular-cli) version 20.2.2.

## Deployment

Assuming the PROFILE argument you specify in the `docker-compose.yml` file in the root of the project repository is set to `prod`:

- Change the frontend config (`src/app/environments/environment.production.ts`) to match the AIoD Keycloak service you use
  - `AIOD_KEYCLOAK_*`: Setup AIoD Keycloak connection
  - `BACKEND_API_URL`: Points to RAIL backend; **keep it as it is**
  - `DEFAULT_PAGE_SIZE`: Defines the default page size on frontend
- Configure AIoD platform URLs in `environment.production.ts`
  - `AIOD_BASE_URL`: Base URL of the AIoD platform
  - `AIOD_EDITOR_URL`: URL of the AIoD Editor service
  - `AIOD_MYLIBRARY_URL`: URL of the AIoD MyLibrary service
  - `AIOD_NAVIGATION_API`: URL of the AIoD navigation API used to build the top menu
- Configure AIoD chatbot integration in `environment.production.ts`
  - `CHATBOT_SCRIPT_SRC`: URL of the chatbot standalone script loaded on the frontend
  - `CHATBOT_ENDPOINT`: Backend endpoint used by the chatbot (RAIL instance)

## Development

To start a local development server, run:

```bash
ng serve
```

Once the server is running, open your browser and navigate to `http://localhost:4200/`. The application will automatically reload whenever you modify any of the source files.

### Code scaffolding

Angular CLI includes powerful code scaffolding tools. To generate a new component, run:

```bash
ng generate component component-name
```

For a complete list of available schematics (such as `components`, `directives`, or `pipes`), run:

```bash
ng generate --help
```

### Building

To build the project run:

```bash
ng build
```

This will compile your project and store the build artifacts in the `dist/` directory. By default, the production build optimizes your application for performance and speed.

### Running unit tests

To execute unit tests with the [Karma](https://karma-runner.github.io) test runner, use the following command:

```bash
ng test
```

### Running end-to-end tests

For end-to-end (e2e) testing, run:

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

### Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
