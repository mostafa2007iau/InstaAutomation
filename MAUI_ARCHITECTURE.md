# .NET MAUI Application: Architectural Blueprint

This document provides a comprehensive architectural blueprint for building the cross-platform mobile and desktop application for the Instagram Automation Bot using .NET MAUI (.NET 9).

---

## 1. Core Architecture & Principles

-   **Pattern:** The application will be built using the **Model-View-ViewModel (MVVM)** pattern. This promotes a clean separation of concerns between the UI (View), the application logic (ViewModel), and the data (Model).
-   **Dependency Injection (DI):** We will use the built-in DI container in .NET MAUI to manage dependencies, making the application modular, testable, and easier to maintain. Services like the `ApiService` will be registered as singletons or transients as appropriate.
-   **Asynchronous Operations:** All network requests and long-running operations will be handled asynchronously (`async/await`) to ensure the UI remains responsive.

## 2. Recommended NuGet Packages

The following NuGet packages are essential for this project:

-   `CommunityToolkit.Mvvm`: A modern, fast, and modular MVVM library. It provides source generators for boilerplate code, `ObservableObject` for data binding, and `RelayCommand` for command handling.
-   `Newtonsoft.Json` or `System.Text.Json`: For serializing and deserializing JSON data when communicating with the backend API.
-   `Microsoft.Extensions.Localization`: For handling multi-language support (Persian/English).
-   `SecureStorage`: .NET MAUI Essentials includes `SecureStorage` for securely storing sensitive data like authentication tokens.

## 3. Project & Folder Structure

A well-organized folder structure is key. Here is the recommended layout:

```
/InstagramAutomationApp
|-- Platforms/          // Platform-specific code
|-- Resources/
|   |-- AppIcon/
|   |-- Fonts/
|   |-- Images/
|   |-- Raw/
|   |-- Splash/
|   |-- Styles/
|   |-- AppResources.resx     // Default (English) strings
|   |-- AppResources.fa.resx  // Persian strings
|-- Converters/         // Value converters for data binding
|-- Models/             // C# classes representing API data (e.g., User, Post, Rule)
|-- Services/
|   |-- IApiService.cs      // Interface for our API service
|   |-- ApiService.cs       // Implementation for API calls
|-- ViewModels/         // ViewModels for each page
|   |-- BaseViewModel.cs
|   |-- LoginPageViewModel.cs
|   |-- DashboardViewModel.cs
|   |-- RuleManagerViewModel.cs
|-- Views/              // XAML pages (the UI)
|   |-- LoginPage.xaml
|   |-- DashboardPage.xaml
|   |-- RuleManagerPage.xaml
|-- App.xaml
|-- AppShell.xaml
|-- MauiProgram.cs      // App startup and service registration
```

## 4. Localization Strategy (Persian & English)

.NET MAUI provides excellent support for localization using RESX files.

-   **Create Resource Files:**
    -   `Resources/AppResources.resx`: This file will contain all the English strings.
    -   `Resources/AppResources.fa.resx`: This file will contain all the Persian strings.
-   **Accessing Strings in XAML:**
    -   Create a static helper class to expose the resource manager.
    -   Use the `x:Static` markup extension in XAML to bind UI text to the localized strings.
        ```xaml
        <Label Text="{x:Static local:AppResources.LoginButtonText}" />
        ```
-   **Switching Languages:** The language can be switched at runtime by setting the `CultureInfo.CurrentUICulture`. A settings page can be added to allow the user to select their preferred language.

## 5. Key Code Samples

### ApiService.cs (Service Layer)

This service will handle all HTTP communication with the Django backend. It will be registered with the DI container.

```csharp
// In Services/ApiService.cs
using System.Net.Http.Json;
using System.Threading.Tasks;

public class ApiService : IApiService
{
    private readonly HttpClient _httpClient;

    public ApiService()
    {
        _httpClient = new HttpClient { BaseAddress = new Uri("http://your_server_ip_or_domain/api/") };
        // Interceptor logic to add JWT token to headers would go here
    }

    public async Task<LoginResponse> LoginAsync(string username, string password)
    {
        var response = await _httpClient.PostAsJsonAsync("token/", new { username, password });
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<LoginResponse>();
    }

    // ... other methods for GetPosts, CreateRule, etc.
}
```

### LoginPageViewModel.cs (ViewModel Layer)

This ViewModel will contain the logic for the login page, including properties for data binding and commands for actions.

```csharp
// In ViewModels/LoginPageViewModel.cs
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using System.Threading.Tasks;

public partial class LoginPageViewModel : ObservableObject
{
    private readonly IApiService _apiService;

    [ObservableProperty]
    private string username;

    [ObservableProperty]
    private string password;

    [ObservableProperty]
    private string errorMessage;

    public LoginPageViewModel(IApiService apiService)
    {
        _apiService = apiService;
    }

    [RelayCommand]
    private async Task LoginAsync()
    {
        try
        {
            ErrorMessage = string.Empty;
            var loginResponse = await _apiService.LoginAsync(Username, Password);

            // Securely store the tokens
            await SecureStorage.SetAsync("accessToken", loginResponse.Access);
            await SecureStorage.SetAsync("refreshToken", loginResponse.Refresh);

            // Navigate to Dashboard
            await Shell.Current.GoToAsync("//DashboardPage");
        }
        catch (Exception ex)
        {
            ErrorMessage = "Login failed. Please check your credentials.";
        }
    }
}
```

### LoginPage.xaml (View Layer)

This is the XAML markup for the UI. It binds to the properties and commands in the `LoginPageViewModel`.

```xaml
<!-- In Views/LoginPage.xaml -->
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:vm="clr-namespace:InstagramAutomationApp.ViewModels"
             x:DataType="vm:LoginPageViewModel"
             x:Class="InstagramAutomationApp.Views.LoginPage">

    <VerticalStackLayout Spacing="15" Padding="30">
        <Label Text="Welcome!" FontSize="Large" HorizontalOptions="Center" />

        <Entry Placeholder="Username" Text="{Binding Username}" />
        <Entry Placeholder="Password" IsPassword="True" Text="{Binding Password}" />

        <Button Text="Login" Command="{Binding LoginCommand}" />

        <Label Text="{Binding ErrorMessage}" TextColor="Red" IsVisible="{Binding ErrorMessage, Converter={StaticResource IsNotNullOrEmptyConverter}}" />
    </VerticalStackLayout>
</ContentPage>
```

## 6. Next Steps

A developer can use this blueprint to:
1.  Set up the .NET MAUI project with the specified structure and NuGet packages.
2.  Implement the full `ApiService` based on the backend API documentation.
3.  Create all the required Models, Views, and ViewModels.
4.  Populate the RESX files with all UI strings for both languages.
5.  Implement navigation using the `AppShell.xaml`.

This architectural guide ensures the development process is structured, scalable, and follows modern best practices.