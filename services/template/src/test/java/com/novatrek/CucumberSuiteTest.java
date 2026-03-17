package com.novatrek;

import org.junit.platform.suite.api.ConfigurationParameter;
import org.junit.platform.suite.api.IncludeEngines;
import org.junit.platform.suite.api.SelectPackages;
import org.junit.platform.suite.api.Suite;

import static io.cucumber.junit.platform.engine.Constants.GLUE_PROPERTY_NAME;
import static io.cucumber.junit.platform.engine.Constants.FEATURES_PROPERTY_NAME;

/**
 * JUnit Platform Suite entry point for Cucumber BDD tests.
 * This class discovers and runs all .feature files under src/test/resources/features/
 * using step definitions from com.novatrek.steps package.
 */
@Suite
@IncludeEngines("cucumber")
@SelectPackages("com.novatrek")
@ConfigurationParameter(key = GLUE_PROPERTY_NAME, value = "com.novatrek.steps")
@ConfigurationParameter(key = FEATURES_PROPERTY_NAME, value = "src/test/resources/features")
public class CucumberSuiteTest {
}
