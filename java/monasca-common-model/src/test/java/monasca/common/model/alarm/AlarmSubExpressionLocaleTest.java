/*
 * Copyright 2015 FUJITSU LIMITED
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */
package monasca.common.model.alarm;

import static org.testng.Assert.assertEquals;

import java.util.Locale;

import org.testng.annotations.BeforeMethod;
import org.testng.annotations.Test;

import com.google.common.collect.ImmutableMap;

import monasca.common.model.metric.MetricDefinition;
/**
 * Checks if conversion from decimal to string is Locale independent.
 *
 * @author lukasz.zajaczkowski@ts.fujitsu.com
 *
 */
@Test
public class AlarmSubExpressionLocaleTest {

  @BeforeMethod
  protected void beforeMethod() {

    // Comma is used as decimal separator for GERMAN locale.
    Locale.setDefault(Locale.GERMAN);
  }

  public void shouldBeLocaleIndependent() {
    AlarmSubExpression alarmSubExpression =
        new AlarmSubExpression(AggregateFunction.MIN, new MetricDefinition("hpcs.compute", ImmutableMap.<String, String>builder()
            .put("instance_id", "5").put("metric_name", "cpu").put("device", "1").build()), AlarmOperator.LT, 1.2, 60, 1);

    assertEquals(alarmSubExpression.getExpression(), "min(hpcs.compute{instance_id=5, metric_name=cpu, device=1}) < 1.2");
  }
}
